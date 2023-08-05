'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const cpp = require("child-process-promise");
const path = require("path");
const sharedStorage_1 = require("../sharedStorage");
const mountedStorageService_1 = require("../storages/mountedStorageService");
const trialConfigMetadataKey_1 = require("../../common/trialConfigMetadataKey");
const log_1 = require("../../../common/log");
const experimentStartupInfo_1 = require("../../../common/experimentStartupInfo");
const INSTALL_NFS_CLIENT = `
#!/bin/bash
if [ -n "$(command -v nfsstat)" ]
then
    exit 0
fi

if [ -n "$(command -v apt-get)" ]
then
    sudo apt-get update
    sudo apt-get install -y nfs-common
elif [ -n "$(command -v yum)" ]
then
    sudo yum install -y nfs-utils
elif [ -n "$(command -v dnf)" ]
then
    sudo dnf install -y nfs-utils
else
    echo "Unknown package management."
    exit 1
fi
`;
class NFSSharedStorageConfig {
    constructor(storageType, localMountPoint, remoteMountPoint, nfsServer, exportedDirectory, localMounted) {
        this.storageType = storageType;
        this.localMountPoint = localMountPoint;
        this.remoteMountPoint = remoteMountPoint;
        this.nfsServer = nfsServer;
        this.exportedDirectory = exportedDirectory;
        this.localMounted = localMounted;
    }
}
class NFSSharedStorageService extends sharedStorage_1.SharedStorageService {
    constructor() {
        super();
        this.log = log_1.getLogger();
        this.internalStorageService = new mountedStorageService_1.MountedStorageService();
        this.experimentId = experimentStartupInfo_1.getExperimentId();
    }
    async config(key, value) {
        if (key === trialConfigMetadataKey_1.TrialConfigMetadataKey.SHARED_STORAGE_CONFIG) {
            const nfsConfig = JSON.parse(value);
            this.localMountPoint = nfsConfig.localMountPoint;
            this.remoteMountPoint = nfsConfig.remoteMountPoint;
            this.storageType = nfsConfig.storageType;
            this.nfsServer = nfsConfig.nfsServer;
            this.exportedDirectory = nfsConfig.exportedDirectory;
            if (nfsConfig.localMounted === 'nnimount') {
                await this.helpLocalMount();
            }
            else if (nfsConfig.localMounted === 'nomount') {
                const errorMessage = `${this.storageType} Shared Storage:  ${this.storageType} not Support 'nomount'.`;
                this.log.error(errorMessage);
                return Promise.reject(errorMessage);
            }
            this.internalStorageService.initialize(this.localMountPoint, path.join(this.localMountPoint, 'nni', this.experimentId));
        }
        return Promise.resolve();
    }
    get canLocalMounted() {
        return true;
    }
    get storageService() {
        return this.internalStorageService;
    }
    get localMountCommand() {
        if (this.localMountPoint) {
            return this.getCommand(this.localMountPoint);
        }
        else {
            this.log.error(`${this.storageType} Shared Storage: localMountPoint is not initialized.`);
            return '';
        }
    }
    get remoteMountCommand() {
        if (this.remoteMountPoint) {
            return this.getCommand(this.remoteMountPoint);
        }
        else {
            this.log.error(`${this.storageType} Shared Storage: remoteMountPoint is not initialized.`);
            return '';
        }
    }
    getCommand(mountPoint) {
        const install = `rm -f nni_install_nfsclient.sh && touch nni_install_nfsclient.sh && echo "${INSTALL_NFS_CLIENT.replace(/\$/g, `\\$`).replace(/\n/g, `\\n`).replace(/"/g, `\\"`)}" >> nni_install_nfsclient.sh && bash nni_install_nfsclient.sh`;
        const mount = `mkdir -p ${mountPoint} && sudo mount ${this.nfsServer}:${this.exportedDirectory} ${mountPoint}`;
        const clean = `rm -f nni_install_nfsclient.sh`;
        return `${install} && ${mount} && ${clean}`;
    }
    get localWorkingRoot() {
        return `${this.localMountPoint}/nni/${this.experimentId}`;
    }
    get remoteWorkingRoot() {
        return `${this.remoteMountPoint}/nni/${this.experimentId}`;
    }
    async helpLocalMount() {
        if (process.platform === 'win32') {
            const errorMessage = `${this.storageType} Shared Storage: NNI not support auto mount ${this.storageType} under Windows yet.`;
            this.log.error(errorMessage);
            return Promise.reject(errorMessage);
        }
        try {
            const result = await cpp.exec(this.localMountCommand);
            if (result.stderr) {
                throw new Error(result.stderr);
            }
        }
        catch (error) {
            const errorMessage = `${this.storageType} Shared Storage: Mount ${this.nfsServer}:${this.exportedDirectory} to ${this.localMountPoint} failed, error is ${error}`;
            this.log.error(errorMessage);
            return Promise.reject(errorMessage);
        }
        return Promise.resolve();
    }
}
exports.NFSSharedStorageService = NFSSharedStorageService;

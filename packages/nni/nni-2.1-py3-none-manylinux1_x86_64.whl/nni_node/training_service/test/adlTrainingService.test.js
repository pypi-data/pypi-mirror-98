'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const chai = require("chai");
const chaiAsPromised = require("chai-as-promised");
const fs = require("fs");
const tmp = require("tmp");
const component = require("../../common/component");
const utils_1 = require("../../common/utils");
const trialConfigMetadataKey_1 = require("../common/trialConfigMetadataKey");
const adlTrainingService_1 = require("../kubernetes/adl/adlTrainingService");
const localCodeDir = tmp.dirSync().name;
describe('Unit Test for AdlTrainingService', () => {
    let skip = false;
    try {
        const testKubeflowConfig = fs.readFileSync('/home/vsts/.kube/config', 'utf8');
    }
    catch (err) {
        console.log('Please have kubernetes cluster to enable its training service unit test.');
        skip = true;
    }
    let testAdlTrialConfig = JSON.stringify({
        "command": "python3 /root/apps/nni_linear_regression/main.py",
        "codeDir": ".",
        "gpuNum": 0,
        "image": "test.image:latest",
        "imagePullSecrets": [
            {
                "name": "stagingsecrets"
            }
        ],
        "nfs": {
            "server": "172.20.188.236",
            "path": "/exports",
            "containerMountPath": "/nfs"
        },
        "memorySize": "1Gi",
        "cpuNum": 1
    });
    let testAdlTrialConfig2 = JSON.stringify({
        "command": "python3 /root/apps/nni_linear_regression/main.py",
        "codeDir": ".",
        "gpuNum": 0,
        "image": "test.image:latest",
        "imagePullSecrets": [
            {
                "name": "stagingsecrets"
            }
        ],
        "adaptive": true,
        "checkpoint": {
            "storageClass": "aws-efs",
            "storageSize": "1Gi"
        },
        "nfs": {
            "server": "172.20.188.236",
            "path": "/exports",
            "containerMountPath": "/nfs"
        }
    });
    let testNniManagerIp = JSON.stringify({
        "nniManagerIp": "0.0.0.0"
    });
    let adlTrainingService;
    console.log(tmp.dirSync().name);
    before(() => {
        chai.should();
        chai.use(chaiAsPromised);
        utils_1.prepareUnitTest();
    });
    after(() => {
        utils_1.cleanupUnitTest();
    });
    beforeEach(() => {
        if (skip) {
            return;
        }
        adlTrainingService = component.get(adlTrainingService_1.AdlTrainingService);
        adlTrainingService.run();
    });
    afterEach(() => {
        if (skip) {
            return;
        }
        adlTrainingService.cleanUp();
    });
    it('Set and get cluster metadata', async () => {
        if (skip) {
            return;
        }
        await adlTrainingService.setClusterMetadata(trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG, testAdlTrialConfig2);
        await adlTrainingService.setClusterMetadata(trialConfigMetadataKey_1.TrialConfigMetadataKey.NNI_MANAGER_IP, testNniManagerIp);
        let data = await adlTrainingService.getClusterMetadata(trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG);
        chai.expect(data).to.be.equals(testAdlTrialConfig2);
    });
    it('Submit job', async () => {
        if (skip) {
            return;
        }
        await adlTrainingService.setClusterMetadata(trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG, testAdlTrialConfig);
        let form = {
            sequenceId: 0,
            hyperParameters: {
                value: 'mock hyperparameters',
                index: 0
            }
        };
        let jobDetail = await adlTrainingService.submitTrialJob(form);
        chai.expect(jobDetail.status).to.be.equals('WAITING');
        await adlTrainingService.cancelTrialJob(jobDetail.id);
        chai.expect(jobDetail.status).to.be.equals('USER_CANCELED');
        await adlTrainingService.setClusterMetadata(trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG, testAdlTrialConfig2);
        form = {
            sequenceId: 0,
            hyperParameters: {
                value: 'mock hyperparameters',
                index: 0
            }
        };
        jobDetail = await adlTrainingService.submitTrialJob(form);
        chai.expect(jobDetail.status).to.be.equals('WAITING');
        await adlTrainingService.cancelTrialJob(jobDetail.id);
        chai.expect(jobDetail.status).to.be.equals('USER_CANCELED');
    }).timeout(3000000);
});

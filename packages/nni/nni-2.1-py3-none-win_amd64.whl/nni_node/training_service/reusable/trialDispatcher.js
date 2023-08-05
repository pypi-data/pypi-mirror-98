'use strict';
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
const events_1 = require("events");
const fs = require("fs");
const path = require("path");
const typescript_ioc_1 = require("typescript-ioc");
const typescript_string_operations_1 = require("typescript-string-operations");
const component = require("../../common/component");
const errors_1 = require("../../common/errors");
const experimentStartupInfo_1 = require("../../common/experimentStartupInfo");
const log_1 = require("../../common/log");
const utils_1 = require("../../common/utils");
const commands_1 = require("../../core/commands");
const gpuData_1 = require("../../training_service/common/gpuData");
const containerJobData_1 = require("../common/containerJobData");
const trialConfigMetadataKey_1 = require("../common/trialConfigMetadataKey");
const util_1 = require("../common/util");
const environment_1 = require("./environment");
const environmentServiceFactory_1 = require("./environments/environmentServiceFactory");
const gpuScheduler_1 = require("./gpuScheduler");
const mountedStorageService_1 = require("./storages/mountedStorageService");
const storageService_1 = require("./storageService");
const sharedStorage_1 = require("./sharedStorage");
const nfsStorageService_1 = require("./shared_storages/nfsStorageService");
const azureblobStorageService_1 = require("./shared_storages/azureblobStorageService");
const trial_1 = require("./trial");
let TrialDispatcher = class TrialDispatcher {
    constructor() {
        this.isDeveloping = false;
        this.stopping = false;
        this.enableVersionCheck = true;
        this.environmentServiceList = [];
        this.environmentMaintenceLoopInterval = -1;
        this.shouldUpdateTrials = true;
        this.enableGpuScheduler = false;
        this.reuseEnvironment = true;
        this.logCollection = '';
        this.isLoggedNoMoreEnvironment = false;
        this.isLoggedNoGpuAvailable = false;
        this.useSharedStorage = false;
        this.fileCopyCompleted = false;
        this.log = log_1.getLogger();
        this.trials = new Map();
        this.environments = new Map();
        this.metricsEmitter = new events_1.EventEmitter();
        this.experimentId = experimentStartupInfo_1.getExperimentId();
        this.experimentRootDir = utils_1.getExperimentRootDir();
        this.commandChannelSet = new Set();
        const logLevel = utils_1.getLogLevel();
        this.log.debug(`current folder ${__dirname}`);
        if (logLevel == "debug" && (fs.existsSync("../../../src/nni_manager") || __dirname.endsWith("src\\nni_manager\\dist\\training_service\\reusable"))) {
            this.log.debug("log level is debug, and exist code folder, so set to developing mode.");
            this.isDeveloping = true;
        }
        this.commandEmitter = new events_1.EventEmitter();
        this.gpuScheduler = new gpuScheduler_1.GpuScheduler();
    }
    async listTrialJobs() {
        const trials = [];
        for (const key of this.trials.keys()) {
            trials.push(await this.getTrialJob(key));
        }
        return trials;
    }
    async getTrialJob(trialJobId) {
        const trial = this.trials.get(trialJobId);
        if (trial === undefined) {
            throw new Error(`trial job ${trialJobId} not found`);
        }
        return trial;
    }
    async getTrialLog(_trialJobId, _logType) {
        throw new errors_1.MethodNotImplementedError();
    }
    async submitTrialJob(form) {
        if (this.trialConfig === undefined) {
            throw new Error(`trialConfig not initialized!`);
        }
        const trialId = utils_1.uniqueString(5);
        const trialJobDetail = new trial_1.TrialDetail(trialId, "WAITING", Date.now(), "", form);
        this.trials.set(trialId, trialJobDetail);
        return trialJobDetail;
    }
    async updateTrialJob(trialJobId, form) {
        const trialDetail = await this.getTrialJob(trialJobId);
        const environment = trialDetail.environment;
        if (environment === undefined) {
            throw new Error(`TrialDispatcher: trial ${trialJobId}'s env shouldn't be undefined in updateTrialJob.`);
        }
        if (environment.environmentService === undefined) {
            throw new Error(`Environment ${environment.id} does not assigned environment service.`);
        }
        const message = {
            "trialId": trialJobId,
            "parameters": form.hyperParameters,
        };
        await environment.environmentService.getCommandChannel.sendCommand(environment, commands_1.SEND_TRIAL_JOB_PARAMETER, message);
        return trialDetail;
    }
    async cancelTrialJob(trialJobId, isEarlyStopped) {
        const trial = await this.getTrialJob(trialJobId);
        switch (trial.status) {
            case "RUNNING":
            case "WAITING":
            case "UNKNOWN":
                {
                    const environment = trial.environment;
                    if (environment && environment.environmentService) {
                        await environment.environmentService.getCommandChannel.sendCommand(environment, commands_1.KILL_TRIAL_JOB, trial.id);
                        trial.isEarlyStopped = isEarlyStopped;
                        trial.status = trial.isEarlyStopped === true ?
                            'EARLY_STOPPED' : 'USER_CANCELED';
                        this.releaseEnvironment(trial);
                    }
                }
                break;
        }
    }
    async run() {
        if (this.trialConfig === undefined) {
            throw new Error(`trial config shouldn't be undefined in run()`);
        }
        for (const environmentService of this.environmentServiceList) {
            const runnerSettings = new environment_1.RunnerSettings();
            runnerSettings.nniManagerIP = this.nniManagerIp === undefined ? utils_1.getIPV4Address() : this.nniManagerIp;
            runnerSettings.nniManagerPort = experimentStartupInfo_1.getBasePort() + 1;
            runnerSettings.commandChannel = environmentService.getCommandChannel.channelName;
            runnerSettings.enableGpuCollector = this.enableGpuScheduler;
            runnerSettings.command = this.trialConfig.command;
            runnerSettings.nniManagerVersion = this.enableVersionCheck ? await utils_1.getVersion() : '';
            runnerSettings.logCollection = this.logCollection;
            runnerSettings.platform = environmentService.getName;
            runnerSettings.experimentId = this.experimentId;
            await environmentService.getCommandChannel.start();
            this.log.info(`TrialDispatcher: started channel: ${environmentService.getCommandChannel.constructor.name}`);
            this.log.info(`TrialDispatcher: copying code and settings.`);
            let storageService;
            if (this.useSharedStorage) {
                if (this.fileCopyCompleted) {
                    this.log.debug(`TrialDispatcher: file already copy to shared storage.`);
                    continue;
                }
                this.log.debug(`TrialDispatcher: use shared storage service.`);
                storageService = component.get(sharedStorage_1.SharedStorageService).storageService;
            }
            else if (environmentService.hasStorageService) {
                this.log.debug(`TrialDispatcher: use existing storage service.`);
                storageService = component.get(storageService_1.StorageService);
            }
            else {
                this.log.debug(`TrialDispatcher: create temp storage service to temp folder.`);
                storageService = new mountedStorageService_1.MountedStorageService();
                const environmentLocalTempFolder = path.join(this.experimentRootDir, "environment-temp");
                storageService.initialize(this.trialConfig.codeDir, environmentLocalTempFolder);
            }
            const codeDir = path.resolve(this.trialConfig.codeDir);
            const envDir = storageService.joinPath("envs");
            const codeFileName = await storageService.copyDirectory(codeDir, envDir, true);
            storageService.rename(codeFileName, "nni-code.tar.gz");
            const installFileName = storageService.joinPath(envDir, 'install_nni.sh');
            await storageService.save(containerJobData_1.CONTAINER_INSTALL_NNI_SHELL_FORMAT, installFileName);
            const runnerSettingsConfig = storageService.joinPath(envDir, "settings.json");
            await storageService.save(JSON.stringify(runnerSettings), runnerSettingsConfig);
            if (this.isDeveloping) {
                let trialToolsPath = path.join(__dirname, "../../../../../tools/nni_trial_tool");
                if (false === fs.existsSync(trialToolsPath)) {
                    trialToolsPath = path.join(__dirname, "..\\..\\..\\..\\..\\tools\\nni_trial_tool");
                }
                await storageService.copyDirectory(trialToolsPath, envDir, true);
            }
            if (this.useSharedStorage) {
                this.fileCopyCompleted = true;
            }
        }
        this.commandEmitter.on("command", (command) => {
            this.handleCommand(command).catch((err) => {
                this.log.error(`TrialDispatcher: error on handle env ${command.environment.id} command: ${command.command}, data: ${command.data}, error: ${err}`);
            });
        });
        await this.prefetchEnvironments();
        this.log.info(`TrialDispatcher: run loop started.`);
        const promiseList = [];
        for (const commandChannel of this.commandChannelSet) {
            promiseList.push(commandChannel.run());
        }
        promiseList.push(this.environmentMaintenanceLoop());
        promiseList.push(this.trialManagementLoop());
        await Promise.all(promiseList);
    }
    addTrialJobMetricListener(listener) {
        this.metricsEmitter.on('metric', listener);
    }
    removeTrialJobMetricListener(listener) {
        this.metricsEmitter.off('metric', listener);
    }
    get isMultiPhaseJobSupported() {
        return true;
    }
    async setClusterMetadata(key, value) {
        switch (key) {
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.NNI_MANAGER_IP:
                this.nniManagerIp = JSON.parse(value).nniManagerIp;
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.VERSION_CHECK:
                this.enableVersionCheck = (value === 'true' || value === 'True');
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.LOG_COLLECTION:
                this.logCollection = value;
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG:
                this.trialConfig = JSON.parse(value);
                if (this.trialConfig.reuseEnvironment !== undefined) {
                    this.reuseEnvironment = this.trialConfig.reuseEnvironment;
                }
                if (this.trialConfig.gpuNum !== undefined && this.trialConfig.gpuNum > 0) {
                    this.log.info(`TrialDispatcher: GPU scheduler is enabled.`);
                    this.enableGpuScheduler = true;
                }
                await util_1.validateCodeDir(this.trialConfig.codeDir);
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.PLATFORM_LIST: {
                const platforms = value.split(",");
                for (const platform of platforms) {
                    const environmentService = environmentServiceFactory_1.EnvironmentServiceFactory.createEnvironmentService(platform);
                    environmentService.initCommandChannel(this.commandEmitter);
                    this.environmentMaintenceLoopInterval =
                        Math.max(environmentService.environmentMaintenceLoopInterval, this.environmentMaintenceLoopInterval);
                    this.commandChannelSet.add(environmentService.getCommandChannel);
                    this.environmentServiceList.push(environmentService);
                }
                break;
            }
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.SHARED_STORAGE_CONFIG:
                if (this.useSharedStorage === false) {
                    await this.initializeSharedStorage(key, value);
                }
                else {
                    const errorMessage = `Already has set shared storage.`;
                    this.log.error(errorMessage);
                }
                break;
        }
        for (const environmentService of this.environmentServiceList) {
            await environmentService.config(key, value);
        }
    }
    getClusterMetadata(_key) {
        throw new Error('Not implemented!');
    }
    async cleanUp() {
        if (this.commandEmitter === undefined) {
            throw new Error(`TrialDispatcher: commandEmitter shouldn't be undefined in cleanUp.`);
        }
        this.stopping = true;
        this.shouldUpdateTrials = true;
        const environments = [...this.environments.values()];
        for (let index = 0; index < environments.length; index++) {
            const environment = environments[index];
            this.log.info(`stopping environment ${environment.id}...`);
            if (environment.environmentService === undefined) {
                throw new Error(`${environment.id} do not have environmentService!`);
            }
            await environment.environmentService.stopEnvironment(environment);
            this.log.info(`stopped environment ${environment.id}.`);
        }
        this.commandEmitter.off("command", this.handleCommand);
        for (const commandChannel of this.commandChannelSet) {
            await commandChannel.stop();
        }
    }
    async environmentMaintenanceLoop() {
        while (!this.stopping) {
            const environments = [];
            for (const environment of this.environments.values()) {
                if (environment.isAlive === true) {
                    environments.push(environment);
                }
                else {
                    if (environment.environmentService === undefined) {
                        throw new Error(`${environment.id} do not have environment service!`);
                    }
                    await environment.environmentService.getCommandChannel.close(environment);
                }
            }
            const environmentServiceDict = new Map();
            for (const environment of environments) {
                if (environment.environmentService === undefined) {
                    throw new Error(`${environment.id} do not have environment service!`);
                }
                if (!environmentServiceDict.has(environment.environmentService)) {
                    environmentServiceDict.set(environment.environmentService, [environment]);
                }
                else {
                    const environmentsList = environmentServiceDict.get(environment.environmentService);
                    if (environmentsList === undefined) {
                        throw new Error(`Environment list not initialized!`);
                    }
                    environmentsList.push(environment);
                    environmentServiceDict.set(environment.environmentService, environmentsList);
                }
            }
            const taskList = [];
            for (const environmentService of environmentServiceDict.keys()) {
                const environmentsList = environmentServiceDict.get(environmentService);
                if (environmentsList) {
                    taskList.push(environmentService.refreshEnvironmentsStatus(environmentsList));
                }
            }
            await Promise.all(taskList);
            for (const environment of environments) {
                if (environment.environmentService === undefined) {
                    throw new Error(`${environment.id} do not have environment service!`);
                }
                const oldIsAlive = environment.isAlive;
                switch (environment.status) {
                    case 'WAITING':
                    case 'RUNNING':
                    case 'UNKNOWN':
                        environment.isAlive = true;
                        break;
                    default:
                        environment.isAlive = false;
                        break;
                }
                if (oldIsAlive !== environment.isAlive) {
                    this.log.debug(`set environment ${environment.id} isAlive from ${oldIsAlive} to ${environment.isAlive} due to status is ${environment.status}.`);
                }
            }
            this.shouldUpdateTrials = true;
            if (this.environmentMaintenceLoopInterval === -1) {
                throw new Error("EnvironmentMaintenceLoopInterval not initialized!");
            }
            await utils_1.delay(this.environmentMaintenceLoopInterval);
        }
    }
    async trialManagementLoop() {
        const interval = 1;
        while (!this.stopping) {
            let totalInterval = 1000;
            while (totalInterval > 0) {
                if (this.shouldUpdateTrials) {
                    this.shouldUpdateTrials = false;
                    break;
                }
                totalInterval -= interval;
                await utils_1.delay(interval);
            }
            const toRefreshedTrials = [];
            for (const trial of this.trials.values()) {
                if (trial.status === "RUNNING" || trial.status === "WAITING" || trial.status === "UNKNOWN") {
                    toRefreshedTrials.push(trial);
                }
            }
            if (toRefreshedTrials.length == 0) {
                continue;
            }
            let waitingTrials = [];
            let liveTrialsCount = 0;
            for (const trial of toRefreshedTrials) {
                const currentStatus = trial.status;
                switch (currentStatus) {
                    case "RUNNING":
                        {
                            const environment = trial.environment;
                            if (environment === undefined) {
                                this.log.error(`found running trial ${trial.id} has no environment, set trial to UNKNOWN.`);
                                trial.status = "UNKNOWN";
                                liveTrialsCount++;
                                continue;
                            }
                            if (environment.environmentService === undefined) {
                                throw new Error(`${environment.id} does not has environment service!`);
                            }
                            trial.url = environment.trackingUrl;
                            const environmentStatus = environment.status;
                            if (trial.nodes.size > 0) {
                                const completedCount = trial.nodes.size;
                                let finalStatus = "SUCCEEDED";
                                let lastTimestamp;
                                this.log.debug(`found ${completedCount} completed trial node(s), nodeCount: ${environment.nodeCount}`);
                                if (environment.nodeCount > completedCount) {
                                    this.log.info(`stop partial completed trial ${trial.id}`);
                                    await environment.environmentService.getCommandChannel.sendCommand(environment, commands_1.KILL_TRIAL_JOB, trial.id);
                                }
                                for (const node of trial.nodes.values()) {
                                    if (node.status === "FAILED") {
                                        finalStatus = "FAILED";
                                    }
                                    if (node.endTime !== undefined) {
                                        if (lastTimestamp === undefined) {
                                            lastTimestamp = node.endTime;
                                        }
                                        else {
                                            lastTimestamp = Math.max(node.endTime, lastTimestamp);
                                        }
                                    }
                                }
                                trial.status = finalStatus;
                                if (lastTimestamp === undefined) {
                                    trial.endTime = lastTimestamp;
                                }
                                this.releaseEnvironment(trial);
                            }
                            else if (environmentStatus !== "RUNNING") {
                                this.log.error(`found running trial ${trial.id} on '${environment.envId}' with '${environmentStatus}', set trial to environment status.`);
                                this.releaseEnvironment(trial);
                                trial.status = environmentStatus;
                            }
                            else {
                                liveTrialsCount++;
                            }
                        }
                        break;
                    case "WAITING":
                    case "UNKNOWN":
                        waitingTrials.push(trial);
                        liveTrialsCount++;
                        break;
                }
            }
            let liveEnvironmentsCount = 0;
            const reusableEnvironments = [];
            for (const environment of this.environments.values()) {
                if (environment.isAlive === true) {
                    liveEnvironmentsCount++;
                    if (environment.status === "RUNNING" && environment.isRunnerReady) {
                        if (0 === environment.runningTrialCount &&
                            false === this.reuseEnvironment &&
                            environment.assignedTrialCount > 0) {
                            if (environment.environmentService === undefined) {
                                throw new Error(`${environment.id} does not has environment service!`);
                            }
                            await environment.environmentService.stopEnvironment(environment);
                            continue;
                        }
                        if (false === this.enableGpuScheduler && environment.runningTrialCount > 0) {
                            continue;
                        }
                        reusableEnvironments.push(environment);
                    }
                }
            }
            let neededEnvironmentCount = 0;
            if (true === this.enableGpuScheduler) {
                let noGpuAvailable = false;
                while (waitingTrials.length > 0) {
                    if (true === noGpuAvailable) {
                        break;
                    }
                    const trial = waitingTrials.shift();
                    if (undefined === trial) {
                        throw new Error(`TrialDispatcher: waiting trial shouldn't be undefined!`);
                    }
                    const gpuNum = this.trialConfig ? this.trialConfig.gpuNum : undefined;
                    const result = this.gpuScheduler.scheduleMachine(reusableEnvironments, gpuNum, trial);
                    switch (result.resultType) {
                        case gpuData_1.ScheduleResultType.REQUIRE_EXCEED_TOTAL:
                            {
                                if (liveEnvironmentsCount == 0) {
                                    this.log.debug(`TrialDispatcher: no live environment, so request one.`);
                                    neededEnvironmentCount = 1;
                                    waitingTrials = [];
                                    this.isLoggedNoGpuAvailable = false;
                                }
                                else if (reusableEnvironments.length > 0) {
                                    const errorMessage = `TrialDispatcher: REQUIRE_EXCEED_TOTAL Required GPU number ${gpuNum} is too large, no machine can meet`;
                                    this.log.error(errorMessage);
                                    throw new errors_1.NNIError(errors_1.NNIErrorNames.RESOURCE_NOT_AVAILABLE, errorMessage);
                                }
                                else {
                                    if (false === this.isLoggedNoGpuAvailable) {
                                        this.log.debug(`TrialDispatcher: wait GPU, live environment ${liveEnvironmentsCount}, no reusable, REQUIRE_EXCEED_TOTAL.`);
                                        this.isLoggedNoGpuAvailable = true;
                                    }
                                }
                                break;
                            }
                        case gpuData_1.ScheduleResultType.TMP_NO_AVAILABLE_GPU:
                            {
                                if (false === this.isLoggedNoGpuAvailable) {
                                    this.log.debug(`TrialDispatcher: wait GPU, live environment ${liveEnvironmentsCount}, reusable ${reusableEnvironments.length}, TMP_NO_AVAILABLE_GPU.`);
                                    this.isLoggedNoGpuAvailable = true;
                                }
                                if (liveEnvironmentsCount <= reusableEnvironments.length) {
                                    neededEnvironmentCount = 1;
                                    this.isLoggedNoGpuAvailable = false;
                                    this.log.info(`TrialDispatcher: ${liveEnvironmentsCount} live env, and ${reusableEnvironments.length} reusable, but no GPU available so request a new one.`);
                                }
                                noGpuAvailable = true;
                            }
                            break;
                        case gpuData_1.ScheduleResultType.SUCCEED:
                            {
                                const environment = result.environment;
                                if (undefined === environment) {
                                    throw new Error(`TrialDispatcher: scheduled env shouldn't be undefined!`);
                                }
                                trial.assignedGpus = result.gpuIndices;
                                await this.allocateEnvironment(trial, environment);
                                this.isLoggedNoGpuAvailable = false;
                            }
                            break;
                        default:
                            throw new Error(`TrialDispatcher: Unknown gpu schecduler type: ${result.resultType}`);
                    }
                }
            }
            else {
                while (reusableEnvironments.length > 0 && waitingTrials.length > 0) {
                    const trial = waitingTrials.shift();
                    const idleEnvironment = reusableEnvironments.shift();
                    if (trial !== undefined && idleEnvironment != undefined) {
                        await this.allocateEnvironment(trial, idleEnvironment);
                    }
                }
                neededEnvironmentCount = liveTrialsCount - liveEnvironmentsCount;
            }
            if (neededEnvironmentCount > 0) {
                let requestedCount = 0;
                let hasMoreEnvironments = false;
                for (let index = 0; index < neededEnvironmentCount; index++) {
                    const environmentService = this.selectEnvironmentService();
                    if (environmentService !== undefined) {
                        hasMoreEnvironments = true;
                        await this.requestEnvironment(environmentService);
                        requestedCount++;
                        this.isLoggedNoMoreEnvironment = false;
                    }
                    else {
                        if (this.isLoggedNoMoreEnvironment === false) {
                            this.isLoggedNoMoreEnvironment = true;
                            this.log.info(`no more environment so far, so skip to request environment.`);
                        }
                    }
                }
                if (hasMoreEnvironments === true || requestedCount > 0) {
                    this.log.info(`requested new environment, live trials: ${liveTrialsCount}, ` +
                        `live environments: ${liveEnvironmentsCount}, neededEnvironmentCount: ${neededEnvironmentCount}, ` +
                        `requestedCount: ${requestedCount}`);
                }
            }
        }
    }
    selectEnvironmentService() {
        const validEnvironmentServiceList = [];
        for (const environmentService of this.environmentServiceList) {
            if (environmentService.hasMoreEnvironments) {
                validEnvironmentServiceList.push(environmentService);
            }
        }
        if (validEnvironmentServiceList.length === 0) {
            return undefined;
        }
        return utils_1.randomSelect(validEnvironmentServiceList);
    }
    async prefetchEnvironments() {
        for (const environmentService of this.environmentServiceList) {
            const number = environmentService.prefetchedEnvironmentCount;
            this.log.info(`Initialize environments total number: ${number}`);
            for (let index = 0; index < number; index++) {
                await this.requestEnvironment(environmentService);
            }
        }
    }
    async requestEnvironment(environmentService) {
        const envId = utils_1.uniqueString(5);
        const envName = `nni_exp_${this.experimentId}_env_${envId}`;
        const environment = environmentService.createEnvironmentInformation(envId, envName);
        environment.environmentService = environmentService;
        this.log.info(`Assign environment service ${environmentService.getName} to environment ${envId}`);
        environment.command = `sh ../install_nni.sh && python3 -m nni.tools.trial_tool.trial_runner`;
        if (this.isDeveloping) {
            environment.command = "[ -d \"nni_trial_tool\" ] && echo \"nni_trial_tool exists already\" || (mkdir ./nni_trial_tool && tar -xof ../nni_trial_tool.tar.gz -C ./nni_trial_tool) && pip3 install websockets && " + environment.command;
        }
        environment.command = `mkdir -p envs/${envId} && cd envs/${envId} && ${environment.command}`;
        environment.useSharedStorage = this.useSharedStorage;
        await environmentService.startEnvironment(environment);
        this.environments.set(environment.id, environment);
        if (environment.status === "FAILED") {
            environment.isAlive = false;
            throw new Error(`error on request environment ${environment.envId}, please check log for more details.`);
        }
        else {
            environment.isAlive = true;
        }
        await environment.environmentService.getCommandChannel.open(environment);
        this.log.info(`requested environment ${environment.id} and job id is ${environment.envId}.`);
    }
    async allocateEnvironment(trial, environment) {
        if (this.trialConfig === undefined) {
            throw new Error(`TrialDispatcher: trialConfig shouldn't be undefined in allocateEnvironment.`);
        }
        if (trial.environment) {
            throw new Error(`TrialDispatcher: trial ${trial.id} has assigned environment ${trial.environment.id} already, not assign to ${environment.id}!`);
        }
        if (environment.runningTrialCount > 0 && false === this.enableGpuScheduler) {
            throw new Error(`TrialDispatcher: environment ${environment.id} has running trial, and gpu scheduler is not enabled, it cannot be assigned again!`);
        }
        this.log.info(`assigning environment ${environment.id} to trial ${trial.id}.`);
        let gpuIndices = undefined;
        if (undefined !== this.trialConfig.gpuNum) {
            const gpuArray = [];
            if (undefined !== trial.assignedGpus) {
                trial.assignedGpus.map((value) => {
                    gpuArray.push(value.index);
                });
            }
            gpuIndices = gpuArray.join(',');
        }
        environment.runningTrialCount++;
        environment.assignedTrialCount++;
        trial.environment = environment;
        if (environment.environmentService === undefined) {
            throw new Error(`${environment.id} environmentService not initialized!`);
        }
        trial.message = `Platform: ${environment.environmentService.getName}, environment: ${environment.id}`;
        if (environment.environmentService.hasStorageService) {
            const storageService = component.get(storageService_1.StorageService);
            trial.workingDirectory = storageService.joinPath('trials', trial.id);
        }
        trial.settings = {
            trialId: trial.id,
            gpuIndices: gpuIndices,
            sequenceId: trial.form.sequenceId,
            parameter: trial.form.hyperParameters,
        };
        trial.startTime = Date.now();
        trial.status = "RUNNING";
        if (environment.environmentService === undefined) {
            throw new Error(`${environment.id} does not have environment service!`);
        }
        await environment.environmentService.getCommandChannel.sendCommand(trial.environment, commands_1.NEW_TRIAL_JOB, trial.settings);
    }
    releaseEnvironment(trial) {
        if (trial.environment !== undefined) {
            if (trial.environment.runningTrialCount <= 0) {
                throw new Error(`TrialDispatcher: environment ${trial.environment.id} has no counted running trial!`);
            }
            trial.environment.runningTrialCount--;
            trial.environment.latestTrialReleasedTime = Date.now();
            trial.environment = undefined;
        }
        if (true === this.enableGpuScheduler) {
            this.gpuScheduler.removeGpuReservation(trial);
        }
    }
    async handleMetricData(trialId, data) {
        if (Array.isArray(data)) {
            for (const subItem of data) {
                this.metricsEmitter.emit('metric', {
                    id: trialId,
                    data: subItem
                });
            }
        }
        else {
            this.metricsEmitter.emit('metric', {
                id: trialId,
                data: data
            });
        }
    }
    async handleStdout(commandData) {
        const metricPattern = /NNISDK_MEb'(?<metrics>.*a?)'$/gm;
        const trialLogDir = path.join(utils_1.getExperimentRootDir(), 'trials', commandData["trial"]);
        utils_1.mkDirPSync(trialLogDir);
        const trialLogPath = path.join(trialLogDir, 'stdout_log_collection.log');
        try {
            let skipLogging = false;
            if (commandData["tag"] === 'trial' && commandData["msg"] !== undefined) {
                const message = commandData["msg"];
                let metricsContent = metricPattern.exec(message);
                while (metricsContent && metricsContent.groups) {
                    const key = 'metrics';
                    const data = metricsContent.groups[key];
                    await this.handleMetricData(commandData["trial"], data);
                    metricsContent = metricPattern.exec(message);
                    skipLogging = true;
                }
            }
            if (!skipLogging) {
                const writeStream = fs.createWriteStream(trialLogPath, {
                    flags: 'a+',
                    encoding: 'utf8',
                    autoClose: true
                });
                writeStream.write(typescript_string_operations_1.String.Format('{0}\n', commandData["msg"]));
                writeStream.end();
            }
        }
        catch (err) {
            this.log.error(`TrialDispatcher: handleStdout error: ${err}`);
        }
    }
    async handleCommand(command) {
        this.log.debug(`TrialDispatcher: env ${command.environment.id} received command ${command.command}.`);
        const environment = command.environment;
        const data = command.data;
        const nodeId = data["node"];
        switch (command.command) {
            case commands_1.REPORT_METRIC_DATA:
                this.log.error(`TrialDispatcher: TODO: not implement to handle direct REPORT_METRIC_DATA command yet.`);
                break;
            case commands_1.STDOUT:
                await this.handleStdout(data);
                break;
            case commands_1.INITIALIZED:
                {
                    let isAllReady = true;
                    if (environment.nodeCount > 1) {
                        let node = environment.nodes.get(nodeId);
                        if (node === undefined) {
                            node = new environment_1.NodeInformation(nodeId);
                            environment.nodes.set(nodeId, node);
                        }
                        const oldNodeStatus = node.status;
                        if (oldNodeStatus === "UNKNOWN" || oldNodeStatus === "WAITING") {
                            node.status = "RUNNING";
                        }
                        if (environment.nodes.size === environment.nodeCount) {
                            for (const node of environment.nodes.values()) {
                                if (node.status !== "RUNNING") {
                                    isAllReady = false;
                                    break;
                                }
                            }
                        }
                        else {
                            isAllReady = false;
                        }
                    }
                    if (isAllReady) {
                        environment.isRunnerReady = true;
                        this.log.info(`TrialDispatcher: env ${environment.id} received initialized message and runner is ready, env status: ${environment.status}.`);
                    }
                }
                break;
            case commands_1.VERSION_CHECK:
                {
                    if (this.enableVersionCheck) {
                        const checkResultSuccess = data["tag"] === 'VCSuccess' ? true : false;
                        if (checkResultSuccess) {
                            this.log.info(`TrialDispatcher: Version check in trialKeeper success!`);
                        }
                        else {
                            const errorMessage = `TrialDispatcher: Version check error, ${data["msg"]}!`;
                            this.log.error(errorMessage);
                        }
                    }
                }
                break;
            case commands_1.GPU_INFO:
                {
                    const gpuData = (data);
                    environment.setGpuSummary(nodeId, gpuData);
                }
                break;
            case commands_1.TRIAL_END:
                {
                    const trialId = data["trial"];
                    const trial = await this.getTrialJob(trialId);
                    const code = parseInt(data["code"]);
                    const timestamp = parseInt(data["time"]);
                    let exitStatus = "SUCCEEDED";
                    if (code !== 0) {
                        exitStatus = "FAILED";
                    }
                    let node = environment.nodes.get(nodeId);
                    if (node === undefined) {
                        node = new environment_1.NodeInformation(nodeId);
                        trial.nodes.set(nodeId, node);
                    }
                    if (undefined === node) {
                        throw new Error("node is impossible to be undefined (see above code), but make eslint happy!");
                    }
                    node.status = exitStatus;
                    node.endTime = timestamp;
                }
                break;
        }
        this.shouldUpdateTrials = true;
    }
    async initializeSharedStorage(key, value) {
        const storageType = JSON.parse(value).storageType;
        switch (storageType) {
            case 'NFS':
                typescript_ioc_1.Container.bind(sharedStorage_1.SharedStorageService)
                    .to(nfsStorageService_1.NFSSharedStorageService)
                    .scope(typescript_ioc_1.Scope.Singleton);
                break;
            case 'AzureBlob':
                typescript_ioc_1.Container.bind(sharedStorage_1.SharedStorageService)
                    .to(azureblobStorageService_1.AzureBlobSharedStorageService)
                    .scope(typescript_ioc_1.Scope.Singleton);
                break;
            default: {
                const errorMessage = `Shared storage type '${storageType}' not support.`;
                this.log.error(errorMessage);
                return Promise.reject(errorMessage);
            }
        }
        await component.get(sharedStorage_1.SharedStorageService).config(key, value);
        this.useSharedStorage = true;
        return Promise.resolve();
    }
};
TrialDispatcher = __decorate([
    component.Singleton,
    __metadata("design:paramtypes", [])
], TrialDispatcher);
exports.TrialDispatcher = TrialDispatcher;

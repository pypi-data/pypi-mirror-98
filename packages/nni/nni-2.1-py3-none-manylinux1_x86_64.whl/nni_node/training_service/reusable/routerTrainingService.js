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
const typescript_ioc_1 = require("typescript-ioc");
const component = require("../../common/component");
const log_1 = require("../../common/log");
const errors_1 = require("../../common/errors");
const utils_1 = require("../../common/utils");
const trialConfigMetadataKey_1 = require("../common/trialConfigMetadataKey");
const paiTrainingService_1 = require("../pai/paiTrainingService");
const remoteMachineTrainingService_1 = require("../remote_machine/remoteMachineTrainingService");
const mountedStorageService_1 = require("./storages/mountedStorageService");
const storageService_1 = require("./storageService");
const trialDispatcher_1 = require("./trialDispatcher");
let RouterTrainingService = class RouterTrainingService {
    constructor() {
        this.log = log_1.getLogger();
    }
    async listTrialJobs() {
        if (this.internalTrainingService === undefined) {
            throw new Error("TrainingService is not assigned!");
        }
        return await this.internalTrainingService.listTrialJobs();
    }
    async getTrialJob(trialJobId) {
        if (this.internalTrainingService === undefined) {
            throw new Error("TrainingService is not assigned!");
        }
        return await this.internalTrainingService.getTrialJob(trialJobId);
    }
    async getTrialLog(_trialJobId, _logType) {
        throw new errors_1.MethodNotImplementedError();
    }
    addTrialJobMetricListener(listener) {
        if (this.internalTrainingService === undefined) {
            throw new Error("TrainingService is not assigned!");
        }
        this.internalTrainingService.addTrialJobMetricListener(listener);
    }
    removeTrialJobMetricListener(listener) {
        if (this.internalTrainingService === undefined) {
            throw new Error("TrainingService is not assigned!");
        }
        this.internalTrainingService.removeTrialJobMetricListener(listener);
    }
    async submitTrialJob(form) {
        if (this.internalTrainingService === undefined) {
            throw new Error("TrainingService is not assigned!");
        }
        return await this.internalTrainingService.submitTrialJob(form);
    }
    async updateTrialJob(trialJobId, form) {
        if (this.internalTrainingService === undefined) {
            throw new Error("TrainingService is not assigned!");
        }
        return await this.internalTrainingService.updateTrialJob(trialJobId, form);
    }
    get isMultiPhaseJobSupported() {
        if (this.internalTrainingService === undefined) {
            throw new Error("TrainingService is not assigned!");
        }
        return this.internalTrainingService.isMultiPhaseJobSupported;
    }
    async cancelTrialJob(trialJobId, isEarlyStopped) {
        if (this.internalTrainingService === undefined) {
            throw new Error("TrainingService is not assigned!");
        }
        await this.internalTrainingService.cancelTrialJob(trialJobId, isEarlyStopped);
    }
    async setClusterMetadata(key, value) {
        if (this.internalTrainingService === undefined) {
            if (key === trialConfigMetadataKey_1.TrialConfigMetadataKey.HYBRID_CONFIG) {
                this.internalTrainingService = component.get(trialDispatcher_1.TrialDispatcher);
                const heterogenousConfig = JSON.parse(value);
                if (this.internalTrainingService === undefined) {
                    throw new Error("internalTrainingService not initialized!");
                }
                if (heterogenousConfig.trainingServicePlatforms.includes('pai')) {
                    typescript_ioc_1.Container.bind(storageService_1.StorageService)
                        .to(mountedStorageService_1.MountedStorageService)
                        .scope(typescript_ioc_1.Scope.Singleton);
                }
                await this.internalTrainingService.setClusterMetadata('platform_list', heterogenousConfig.trainingServicePlatforms.join(','));
            }
            else if (key === trialConfigMetadataKey_1.TrialConfigMetadataKey.LOCAL_CONFIG) {
                this.internalTrainingService = component.get(trialDispatcher_1.TrialDispatcher);
                if (this.internalTrainingService === undefined) {
                    throw new Error("internalTrainingService not initialized!");
                }
                await this.internalTrainingService.setClusterMetadata('platform_list', 'local');
            }
            else if (key === trialConfigMetadataKey_1.TrialConfigMetadataKey.PAI_CLUSTER_CONFIG) {
                const config = JSON.parse(value);
                if (config.reuse === true) {
                    this.log.info(`reuse flag enabled, use EnvironmentManager.`);
                    this.internalTrainingService = component.get(trialDispatcher_1.TrialDispatcher);
                    typescript_ioc_1.Container.bind(storageService_1.StorageService)
                        .to(mountedStorageService_1.MountedStorageService)
                        .scope(typescript_ioc_1.Scope.Singleton);
                    if (this.internalTrainingService === undefined) {
                        throw new Error("internalTrainingService not initialized!");
                    }
                    await this.internalTrainingService.setClusterMetadata('platform_list', 'pai');
                }
                else {
                    this.log.debug(`caching metadata key:{} value:{}, as training service is not determined.`);
                    this.internalTrainingService = component.get(paiTrainingService_1.PAITrainingService);
                }
            }
            else if (key === trialConfigMetadataKey_1.TrialConfigMetadataKey.AML_CLUSTER_CONFIG) {
                this.internalTrainingService = component.get(trialDispatcher_1.TrialDispatcher);
                if (this.internalTrainingService === undefined) {
                    throw new Error("internalTrainingService not initialized!");
                }
                await this.internalTrainingService.setClusterMetadata('platform_list', 'aml');
            }
            else if (key === trialConfigMetadataKey_1.TrialConfigMetadataKey.REMOTE_CONFIG) {
                const config = JSON.parse(value);
                if (config.reuse === true) {
                    this.log.info(`reuse flag enabled, use EnvironmentManager.`);
                    this.internalTrainingService = component.get(trialDispatcher_1.TrialDispatcher);
                    if (this.internalTrainingService === undefined) {
                        throw new Error("internalTrainingService not initialized!");
                    }
                    await this.internalTrainingService.setClusterMetadata('platform_list', 'remote');
                }
                else {
                    this.log.debug(`caching metadata key:{} value:{}, as training service is not determined.`);
                    this.internalTrainingService = component.get(remoteMachineTrainingService_1.RemoteMachineTrainingService);
                }
            }
        }
        if (this.internalTrainingService === undefined) {
            throw new Error("internalTrainingService not initialized!");
        }
        await this.internalTrainingService.setClusterMetadata(key, value);
    }
    async getClusterMetadata(key) {
        if (this.internalTrainingService === undefined) {
            throw new Error("TrainingService is not assigned!");
        }
        return await this.internalTrainingService.getClusterMetadata(key);
    }
    async cleanUp() {
        if (this.internalTrainingService === undefined) {
            throw new Error("TrainingService is not assigned!");
        }
        await this.internalTrainingService.cleanUp();
    }
    async run() {
        while (this.internalTrainingService === undefined) {
            await utils_1.delay(100);
        }
        return await this.internalTrainingService.run();
    }
};
RouterTrainingService = __decorate([
    component.Singleton,
    __metadata("design:paramtypes", [])
], RouterTrainingService);
exports.RouterTrainingService = RouterTrainingService;

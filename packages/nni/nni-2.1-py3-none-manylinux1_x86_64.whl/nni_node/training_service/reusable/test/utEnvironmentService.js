"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const environment_1 = require("../environment");
const utCommandChannel_1 = require("./utCommandChannel");
class UtEnvironmentService extends environment_1.EnvironmentService {
    constructor() {
        super();
        this.allEnvironments = new Map();
        this.hasMoreEnvironmentsInternal = true;
    }
    get hasStorageService() {
        return false;
    }
    get useSharedStorage() {
        return false;
    }
    get environmentMaintenceLoopInterval() {
        return 1;
    }
    get getName() {
        return 'ut';
    }
    initCommandChannel(eventEmitter) {
        this.commandChannel = new utCommandChannel_1.UtCommandChannel(eventEmitter);
    }
    testSetEnvironmentStatus(environment, newStatus) {
        environment.status = newStatus;
    }
    testReset() {
        this.allEnvironments.clear();
    }
    testGetEnvironments() {
        return this.allEnvironments;
    }
    testSetNoMoreEnvironment(hasMore) {
        this.hasMoreEnvironmentsInternal = hasMore;
    }
    get hasMoreEnvironments() {
        return this.hasMoreEnvironmentsInternal;
    }
    async config(_key, _value) {
    }
    async refreshEnvironmentsStatus(environments) {
    }
    async startEnvironment(environment) {
        if (!this.allEnvironments.has(environment.id)) {
            this.allEnvironments.set(environment.id, environment);
            environment.status = "WAITING";
        }
    }
    async stopEnvironment(environment) {
        environment.status = "USER_CANCELED";
    }
}
exports.UtEnvironmentService = UtEnvironmentService;

"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const amlEnvironmentService_1 = require("./amlEnvironmentService");
const openPaiEnvironmentService_1 = require("./openPaiEnvironmentService");
const localEnvironmentService_1 = require("./localEnvironmentService");
const remoteEnvironmentService_1 = require("./remoteEnvironmentService");
class EnvironmentServiceFactory {
    static createEnvironmentService(name) {
        switch (name) {
            case 'local':
                return new localEnvironmentService_1.LocalEnvironmentService();
            case 'remote':
                return new remoteEnvironmentService_1.RemoteEnvironmentService();
            case 'aml':
                return new amlEnvironmentService_1.AMLEnvironmentService();
            case 'pai':
                return new openPaiEnvironmentService_1.OpenPaiEnvironmentService();
            default:
                throw new Error(`${name} not supported!`);
        }
    }
}
exports.EnvironmentServiceFactory = EnvironmentServiceFactory;

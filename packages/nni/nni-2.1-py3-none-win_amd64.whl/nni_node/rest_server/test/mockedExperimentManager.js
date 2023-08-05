'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const experimentManager_1 = require("../../common/experimentManager");
exports.testExperimentManagerProvider = {
    get: () => { return new mockedeExperimentManager(); }
};
class mockedeExperimentManager extends experimentManager_1.ExperimentManager {
    getExperimentsInfo() {
        const expInfo = JSON.parse(JSON.stringify({
            "test": {
                "port": 8080,
                "startTime": 1605246730756,
                "endTime": "N/A",
                "status": "RUNNING",
                "platform": "local",
                "experimentName": "testExp",
                "tag": [], "pid": 11111,
                "webuiUrl": [],
                "logDir": null
            }
        }));
        return new Promise((resolve, reject) => {
            resolve(expInfo);
        });
    }
    setExperimentPath(newPath) {
        return;
    }
    setExperimentInfo(experimentId, key, value) {
        return;
    }
    stop() {
        return new Promise(() => { });
    }
}
exports.mockedeExperimentManager = mockedeExperimentManager;

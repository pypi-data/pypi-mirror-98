'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const chai_1 = require("chai");
const fs = require("fs");
const typescript_ioc_1 = require("typescript-ioc");
const component = require("../../common/component");
const utils_1 = require("../../common/utils");
const experimentManager_1 = require("../../common/experimentManager");
const nniExperimentsManager_1 = require("../nniExperimentsManager");
describe('Unit test for experiment manager', function () {
    let experimentManager;
    const mockedInfo = {
        "test": {
            "port": 8080,
            "startTime": 1605246730756,
            "endTime": "N/A",
            "status": "INITIALIZED",
            "platform": "local",
            "experimentName": "testExp",
            "tag": [], "pid": 11111,
            "webuiUrl": [],
            "logDir": null
        }
    };
    before(() => {
        utils_1.prepareUnitTest();
        fs.writeFileSync('.experiment.test', JSON.stringify(mockedInfo));
        typescript_ioc_1.Container.bind(experimentManager_1.ExperimentManager).to(nniExperimentsManager_1.NNIExperimentsManager).scope(typescript_ioc_1.Scope.Singleton);
        experimentManager = component.get(nniExperimentsManager_1.NNIExperimentsManager);
        experimentManager.setExperimentPath('.experiment.test');
    });
    after(() => {
        if (fs.existsSync('.experiment.test')) {
            fs.unlinkSync('.experiment.test');
        }
        utils_1.cleanupUnitTest();
    });
    it('test getExperimentsInfo', () => {
        return experimentManager.getExperimentsInfo().then(function (experimentsInfo) {
            new Array(experimentsInfo);
            for (let idx in experimentsInfo) {
                if (experimentsInfo[idx]['id'] === 'test') {
                    chai_1.expect(experimentsInfo[idx]['status']).to.be.oneOf(['STOPPED', 'ERROR']);
                    break;
                }
            }
        }).catch((error) => {
            chai_1.assert.fail(error);
        });
    });
});

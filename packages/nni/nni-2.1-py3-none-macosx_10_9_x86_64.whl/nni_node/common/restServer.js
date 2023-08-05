'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const express = require("express");
const ts_deferred_1 = require("ts-deferred");
const log_1 = require("./log");
const experimentStartupInfo_1 = require("./experimentStartupInfo");
class RestServer {
    constructor() {
        this.hostName = '0.0.0.0';
        this.app = express();
        this.log = log_1.getLogger();
        this.port = experimentStartupInfo_1.getBasePort();
        assert(this.port && this.port > 1024);
    }
    get endPoint() {
        return `http://${this.hostName}:${this.port}`;
    }
    start(hostName) {
        this.log.info(`RestServer start`);
        if (this.startTask !== undefined) {
            return this.startTask.promise;
        }
        this.startTask = new ts_deferred_1.Deferred();
        this.registerRestHandler();
        if (hostName) {
            this.hostName = hostName;
        }
        this.log.info(`RestServer base port is ${this.port}`);
        this.server = this.app.listen(this.port, this.hostName).on('listening', () => {
            this.startTask.resolve();
        }).on('error', (e) => {
            this.startTask.reject(e);
        });
        return this.startTask.promise;
    }
    stop() {
        if (this.stopTask !== undefined) {
            return this.stopTask.promise;
        }
        this.stopTask = new ts_deferred_1.Deferred();
        if (this.startTask === undefined) {
            this.stopTask.resolve();
            return this.stopTask.promise;
        }
        else {
            this.startTask.promise.then(() => {
                this.server.close().on('close', () => {
                    this.log.info('Rest server stopped.');
                    this.stopTask.resolve();
                }).on('error', (e) => {
                    this.log.error(`Error occurred stopping Rest server: ${e.message}`);
                    this.stopTask.reject();
                });
            }, () => {
                this.stopTask.resolve();
            });
        }
        this.stopTask.resolve();
        return this.stopTask.promise;
    }
}
exports.RestServer = RestServer;

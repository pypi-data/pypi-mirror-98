/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { App } from './App';
import { Status } from './Module';

import { ISignal, Signal } from '@lumino/signaling';
import { Global } from '../Global';

import { ServerConnection } from '@jupyterlab/services';

export class AppTracker {
	private _polling = false;

	private _apps: App[] = [];
	private _appsChanged = new Signal<this, App[]>(this);

	constructor() {
		this._polling = true;
		this.receiveAppUpdates();
		this.receiveModuleUpdates();

		for (var app of this.activeSessions) {
			for (var module of app.modules) {
				module.startSessionHandler();
			}
		}
	}

	get appsChanged(): ISignal<this, App[]> {
		return this._appsChanged;
	}

	get activeJobsOrSessions(): App[] {
		return this._apps.filter((app: App) => app.getAppStatus() != Status.Completed);
	}

	get activeSessions(): App[] {
		return this._apps.filter((app: App) => app.getAppStatus() != Status.Completed && app.interactive);
	}

	get finishedSessions(): App[] {
		return this._apps.filter((app: App) => app.getAppStatus() == Status.Completed && app.interactive);
	}

	get activeJobs(): App[] {
		return this._apps.filter((app: App) => app.getAppStatus() != Status.Completed && !app.interactive);
	}

	get finishedJobs(): App[] {
		return this._apps.filter((app: App) => app.getAppStatus() == Status.Completed && !app.interactive);
	}

	public addApp(app: App) {
		this._apps.unshift(app);
		if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
		this._appsChanged.emit(this._apps);
		app.changed.connect(() => {
			if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
			return this._appsChanged.emit(this._apps)
		}, this);
	}

	public removeApp(uuid: string) {
		var app: App = this._apps.filter((app: App) => app.uuid == uuid)[0];
		this._apps = this._apps.filter((app: App) => app.uuid != uuid);
		app.changed.disconnect(() => {
			if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
			return this._appsChanged.emit(this._apps)
		}, this);
		if (Global.shouldLogOnEmit) console.log('SignalEmit (' + new Date().getSeconds() + ')');
		this._appsChanged.emit(this._apps);
	}

	public getDisplayNum() {
		return this._apps.filter((app: App) => app.getAppStatus() != Status.Completed).length;
	}

	// If we are polling, send a new request 2 seconds after completing the previous request
	private  appPollDelay = 2000;
	private receiveAppUpdates() {
		if (!this._polling) return;
		// If there is an unsigned agreement, do not poll
        if (Global.user != null && Global.user.unsignedAgreement) {
			if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
			setTimeout(() => this.receiveAppUpdates(), this.appPollDelay);
            return;
        }
		const uuids: string[] = [];
		const lastInitializingLines: number[] = [];
		const lastUploadingLines: number[] = [];
		const lastRequisitioningLines: number[] = [];
		const lastRunningLines: number[] = [];
		for (var app of this.activeJobsOrSessions) {
			uuids.push(app.uuid);
			lastInitializingLines.push(app.initializing.length);
			lastUploadingLines.push(app.uploading.length);
			lastRequisitioningLines.push(app.requisitioning.length);
			lastRunningLines.push(app.running.length);
		}
		// There is no need to make an empty request
		if (uuids.length > 0) {
			const settings = ServerConnection.makeSettings();
			const url = settings.baseUrl + "optumi/pull-workload-status-updates";
			const init: RequestInit = {
				method: 'POST',
				body: JSON.stringify({
					uuids: uuids,
					lastInitializingLines: lastInitializingLines,
					lastUploadingLines: lastUploadingLines,
					lastRequisitioningLines: lastRequisitioningLines,
					lastRunningLines: lastRunningLines,
				}),
			};
			ServerConnection.makeRequest(
				url,
				init, 
				settings
			).then((response: Response) => {
				if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
				setTimeout(() => this.receiveAppUpdates(), this.appPollDelay);
				Global.handleResponse(response);
				return response.json();
			}).then((body: any) => {
				for (var app of this._apps) {
					if (body[app.uuid]) {
						app.handleUpdate(body[app.uuid]);
					}
				}
			});
		} else {
			if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
			setTimeout(() => this.receiveAppUpdates(), this.appPollDelay);
		}
	}
	// If we are polling, send a new request 2 seconds after completing the previous request
	private modPollingDelay = 500;
	private async receiveModuleUpdates() {
		if (!this._polling) return;
        // If there is an unsigned agreement, do not poll
        if (Global.user != null && Global.user.unsignedAgreement) {
			if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
			setTimeout(() => this.receiveModuleUpdates(), this.modPollingDelay);
            return;
        }
		const workloadUUIDs: string[] = [];
		const moduleUUIDs: string[] = [];
		const lastUpdateLines: number[] = [];
		const lastOutputLines: number[] = [];
		for (var app of this._apps) {
			for (var module of app.modules) {
				// NOTE: Due to the separation of apps and modules state, there can be an active module in a completed app 
				if (module.modStatus != Status.Completed) {
					workloadUUIDs.push(app.uuid);
					moduleUUIDs.push(module.uuid);
					lastUpdateLines.push(module.updates.length);
					lastOutputLines.push(module.output.length);
				}
			}
		}
		// There is no need to make an empty request
		if (workloadUUIDs.length > 0) {
			const settings = ServerConnection.makeSettings();
			const url = settings.baseUrl + "optumi/pull-module-status-updates";
			const init: RequestInit = {
				method: 'POST',
				body: JSON.stringify({
					workloadUUIDs: workloadUUIDs,
					moduleUUIDs: moduleUUIDs,
					lastUpdateLines: lastUpdateLines,
					lastOutputLines: lastOutputLines,
				}),
			};
			ServerConnection.makeRequest(
				url,
				init, 
				settings
			).then((response: Response) => {
				if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
				setTimeout(() => this.receiveModuleUpdates(), this.modPollingDelay);
				Global.handleResponse(response);
				return response.json();
			}).then((body: any) => {
				for (var app of this._apps) {
					for (var module of app.modules) {
						if (body[module.uuid]) {
							module.handleUpdate(body[module.uuid]);
						}
					}
				}
			});
		} else {
			if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
			setTimeout(() => this.receiveModuleUpdates(), this.modPollingDelay);
		}
	}

	public stopPolling() {
		this._polling = false;
		for (var app of this.activeSessions) {
			for (var module of app.modules) {
				module.stopSessionHandler();
			}
		}
	}
}

/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../../Global';

import { ServerConnection } from '@jupyterlab/services';

interface IProps {
    style?: React.CSSProperties
}

interface IState {
    cost: number,
    balance: number,
}

export class Credits extends React.Component<IProps, IState> {
    private _isMounted = false;
    private polling = false;

    constructor(props: IProps) {
        super(props);
        this.state = {
            cost: Global.lastCreditsCost,
            balance: Global.lastCreditsBalance,
        }
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');

        return (
            <div style={{display: 'flex', margin: '6px'}}>
                <div style={{flexGrow: 1, justifyContent: 'center', fontSize: '16px', lineHeight: '30px', fontWeight: 'bold'}}>
                    Credits
                </div>
                <div style={{flexGrow: 1, justifyContent: 'center', fontSize: '14px', lineHeight: '30px', textAlign: 'right'}}>
                    <div>
                        Left: ${(-this.state.balance).toFixed(2)} 
                    </div>
                    <div>
                        Used: ${this.state.cost.toFixed(2)}
                    </div>
                </div>
            </div>
        )
    }


    private previousUpdate: any
    private async receiveUpdate() {
		const settings = ServerConnection.makeSettings();
        const url = settings.baseUrl + "optumi/get-total-billing";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				startTime: new Date(0).toISOString(),
				endTime: new Date().toISOString(),
			}),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			if (this.polling) {
				// If we are polling, send a new request in 2 seconds
                if (Global.shouldLogOnPoll) console.log('FunctionPoll (' + new Date().getSeconds() + ')');
				setTimeout(() => this.receiveUpdate(), 2000);
			}
            Global.handleResponse(response);
			return response.json();
		}).then((body: any) => {
			if (body) {
				if (JSON.stringify(body) !== JSON.stringify(this.previousUpdate)) {
                    this.safeSetState({ balance: body.balance, cost: body.total });
                    this.previousUpdate = body
                }
			}
		});
	}

    // Will be called automatically when the component is mounted
	public componentDidMount = () => {
        this._isMounted = true;
        this.polling = true;
        this.receiveUpdate();
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
        this._isMounted = false;
        Global.lastCreditsCost = this.state.cost;
        Global.lastCreditsBalance = this.state.balance;
        this.polling = false;
    }
    
    private safeSetState = (map: any) => {
		if (this._isMounted) {
			let update = false
			try {
				for (const key of Object.keys(map)) {
					if (JSON.stringify(map[key]) !== JSON.stringify((this.state as any)[key])) {
						update = true
						break
					}
				}
			} catch (error) {
				update = true
			}
			if (update) {
				if (Global.shouldLogOnSafeSetState) console.log('SafeSetState (' + new Date().getSeconds() + ')');
				this.setState(map)
			} else {
				if (Global.shouldLogOnSafeSetState) console.log('SuppressedSetState (' + new Date().getSeconds() + ')');
			}
		}
	}
    
    public shouldComponentUpdate = (nextProps: IProps, nextState: IState): boolean => {
        try {
            if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
            if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
            if (Global.shouldLogOnRender) console.log('SuppressedRender (' + new Date().getSeconds() + ')');
            return false;
        } catch (error) {
            return true;
        }
    }
}

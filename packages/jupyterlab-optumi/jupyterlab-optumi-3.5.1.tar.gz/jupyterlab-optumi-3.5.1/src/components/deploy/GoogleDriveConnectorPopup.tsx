/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { CSSProperties } from '@material-ui/core/styles/withStyles';
import * as React from 'react'
import { Global } from '../../Global';
import { TextBox } from '../../core';

import { DataService } from './dataConnectorBrowser/DataConnectorDirListingItemIcon';
import { BaseConnectorPopup } from '../../core/BaseConnectorPopup';

interface IProps {
    // This close action will allow us to get a new set of connectors when a new one is created
    onClose?: () => any
    style?: CSSProperties
}

interface IState {
    fileID: string
    serviceAccountKey: string
}

const defaultState = {
    fileID: '',
    serviceAccountKey: '',
}

export class GoogleDriveConnectorPopup extends React.Component<IProps, IState> {
    private _isMounted = false

    constructor(props: IProps) {
        super(props);
		this.state = defaultState;
    }

	private handleClose = () => {
        if (this.props.onClose) this.props.onClose();
        this.safeSetState(defaultState);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <BaseConnectorPopup
                dataService={DataService.GOOGLE_DRIVE}
                iconClass='jp-drive-logo'
                description='Access a Drive file'
                header='Connect to a Google Drive file using a Service Account.'
                downloadPath='~/gdrive/'
                onClose={this.handleClose}
                getInfo={() => this.state}
                getContents={(waiting: boolean) => (
                    <>
                        <TextBox<string>
                            getValue={() => this.state.fileID}
                            saveValue={(value: string) => this.safeSetState({ fileID: value })}
                            label='File ID'
                            helperText='The unique ID found in the sharable link.'
                            labelWidth={BaseConnectorPopup.LABEL_WIDTH}
                            disabled={waiting}
                            required
                        />
                        <TextBox<string>
                            getValue={() => this.state.serviceAccountKey}
                            saveValue={(value: string) => this.safeSetState({ serviceAccountKey: value })}
                            label='Service Account Key'
                            helperText='The contents of the credentials file generated for your Google Service Account.'
                            labelWidth={BaseConnectorPopup.LABEL_WIDTH}
                            disabled={waiting}
                            multiline
                            minLines={5}
                        />
                    </>
                )}
            />
        )
    }

    public componentDidMount = () => {
        this._isMounted = true
    }

    public componentWillUnmount = () => {
        this._isMounted = false
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
}

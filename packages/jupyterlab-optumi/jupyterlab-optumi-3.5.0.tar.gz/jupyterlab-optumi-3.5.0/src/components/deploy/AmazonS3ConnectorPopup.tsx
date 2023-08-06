/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { CSSProperties } from '@material-ui/core/styles/withStyles';
import * as React from 'react'
import { Global } from '../../Global';
import { Dropdown, TextBox } from '../../core';

import { DataService } from './dataConnectorBrowser/DataConnectorDirListingItemIcon';
import { BaseConnectorPopup } from '../../core/BaseConnectorPopup';
import { AWSRegions } from '../../models/AWSRegions';

interface IProps {
    // This close action will allow us to get a new set of connectors when a new one is created
    onClose?: () => any
    style?: CSSProperties
}

interface IState {
    region: string
    bucketName: string
    objectKey: string
    accessKeyID: string
    accessSecretKey: string
}

const defaultState = {
    region: AWSRegions.US_EAST_1.region,
    bucketName: '',
    objectKey: '',
    accessKeyID: '',
    accessSecretKey: '',
}

export class AmazonS3ConnectorPopup extends React.Component<IProps, IState> {
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
                dataService={DataService.AMAZON_S3}
                iconClass='jp-s3-logo'
                description='Access an S3 bucket'
                header='Connect to an Amazon S3 bucket or object.'
                downloadPath='~/s3/'
                onClose={this.handleClose}
                getInfo={() => this.state}
                getContents={(waiting: boolean) => (
                    <>
                        <Dropdown
                            getValue={() => this.state.region}
                            saveValue={(value: string) => this.safeSetState({ region: value })}
                            label='Region'
                            labelWidth={BaseConnectorPopup.LABEL_WIDTH}
                            values={AWSRegions.values.map(x => { return { value: x.region, description: x.description} })}
                            helperText='The service region as specified in S3 documentation.'
                        />
                        <TextBox<string>
                            getValue={() => this.state.bucketName}
                            saveValue={(value: string) => this.safeSetState({ bucketName: value })}
                            label='Bucket Name'
                            helperText='The Bucket Name as specified in S3 documentation.'
                            labelWidth={BaseConnectorPopup.LABEL_WIDTH}
                            disabled={waiting}
                            required
                        />
                        <TextBox<string>
                            getValue={() => this.state.objectKey}
                            saveValue={(value: string) => this.safeSetState({ objectKey: value })}
                            label='Object Key'
                            helperText='If you leave this blank, we will transfer the entire bucket.'
                            labelWidth={BaseConnectorPopup.LABEL_WIDTH}
                            disabled={waiting}
                        />
                        <TextBox<string>
                            getValue={() => this.state.accessKeyID}
                            saveValue={(value: string) => this.safeSetState({ accessKeyID: value })}
                            label='Access Key ID'
                            helperText='The Access Key ID as specified in S3 documentation.'
                            labelWidth={BaseConnectorPopup.LABEL_WIDTH}
                            disabled={waiting}
                            required
                        />
                        <TextBox<string>
                            getValue={() => this.state.accessSecretKey}
                            saveValue={(value: string) => this.safeSetState({ accessSecretKey: value })}
                            label='Access Secret Key'
                            helperText='The Access Secret Key as specified in S3 documentation.'
                            labelWidth={BaseConnectorPopup.LABEL_WIDTH}
                            disabled={waiting}
                            required
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

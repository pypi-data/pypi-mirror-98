/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import DataConnectorDirListingItemIcon, { DataService } from './DataConnectorDirListingItemIcon'
import { DataConnectorMetadata } from './DataConnectorBrowser'
import { Button, withStyles } from '@material-ui/core'
import { Global } from '../../../Global';

const StyledButton = withStyles({
    root: {
        display: 'inline-block',
        height: '20px',
        padding: '3px 6px',
        lineHeight: '12px',
        fontSize: '12px',
        minWidth: '0px',
        margin: 'auto',
    },
 })(Button);

 interface DataConnectorType {
    dataService: DataService,
    provider: string,
    service: string,
}

const dataConnectorTypes: DataConnectorType[] = [
    {dataService: DataService.AMAZON_S3,            provider: 'Amazon', service: 'S3'},
    {dataService: DataService.WASABI,               provider: 'Wasabi', service: ''},
    {dataService: DataService.GOOGLE_DRIVE,         provider: 'Google', service: 'Drive'},
    {dataService: DataService.GOOGLE_CLOUD_STORAGE, provider: 'Google', service: 'Cloud Storage'},
    {dataService: DataService.KAGGLE,               provider: 'Kaggle', service: ''},
    {dataService: DataService.EMPTY,                provider: '', service: '--'},
]

interface IProps {
    dataConnectorMetadata: DataConnectorMetadata
    selected: boolean
    onClick: (event: React.MouseEvent<HTMLLIElement, MouseEvent>) => void
    onDoubleClick: (event: React.MouseEvent<HTMLLIElement, MouseEvent>) => void
    handleButtonClick?: (dataConnectorMetadata: DataConnectorMetadata) => void
    buttonColor?: string
    buttonText?: string
}

interface IState {}

export default class DataConnectorDirListingItem extends React.Component<IProps, IState> {

    constructor(props: IProps) {
        super(props)
        this.state = {
            focused: false
        }
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        const dataConnectorMetadata = this.props.dataConnectorMetadata
        return (
            <li
                className={'jp-DirListing-item' + (this.props.selected ? ' jp-mod-selected' : '')}
                style={{lineHeight: '25px', padding: '4px 17px'}}
                onClick={(event: React.MouseEvent<HTMLLIElement, MouseEvent>) => this.props.onClick(event)}
                onDoubleClick={(event: React.MouseEvent<HTMLLIElement, MouseEvent>) => this.props.onDoubleClick(event)}
            >
                <DataConnectorDirListingItemIcon
                    style={{
                        margin: '2.5px auto',
                        width: '20px',
                        height: '20px',
                    }}
                    dataService={dataConnectorMetadata.dataService} 
                />
                <span className='jp-DirListing-itemModified' 
                    style={
                        dataConnectorMetadata.dataService == DataService.EMPTY ? {
                            textAlign: 'left',
                            flex: '0 0 185px',
                            marginLeft: '-24px',
                            marginRight: '24px',
                        } : {
                            textAlign: 'left',
                            flex: '0 0 185px',
                            marginLeft: '8px'
                        }
                    }
                >
                    {(() => {
                        for (const dataConnectorType of dataConnectorTypes) {
                            if (dataConnectorType.dataService === dataConnectorMetadata.dataService) {
                                return (
                                    <>
                                        <span style={{fontWeight: 'bold', marginRight: '0.25em'}}>
                                            {dataConnectorType.provider}
                                        </span>
                                        {dataConnectorType.service}
                                    </>
                                )
                            }
                        }
                        return <span />
                    })()}
                </span>
                <span className='jp-DirListing-itemText'>
                    {dataConnectorMetadata.name}
                </span>
                {this.props.handleButtonClick && this.props.buttonColor && this.props.buttonText && (
                    <StyledButton
                        onClick={() => this.props.handleButtonClick(this.props.dataConnectorMetadata)}
                        variant='outlined'
                        color='primary'
                        disableElevation
                        style={{
                            color: this.props.buttonColor,
                            border: '1px solid ' + this.props.buttonColor,
                        }}
                    >
                        {this.props.buttonText}
                    </StyledButton>
                )}
            </li>
        )
    }
}
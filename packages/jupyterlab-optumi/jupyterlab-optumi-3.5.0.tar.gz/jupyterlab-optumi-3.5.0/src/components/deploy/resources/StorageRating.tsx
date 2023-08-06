/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../../../Global';

import { Slider } from '../../../core';
import { OptumiMetadataTracker } from '../../../models/OptumiMetadataTracker';
import { StorageMetadata } from '../../../models/StorageMetadata';
import FormatUtils from '../../../utils/FormatUtils';

interface IProps {
    style?: React.CSSProperties,
}

interface IState {}

export class StorageRating extends React.Component<IProps, IState> {

    private getValue(): number {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const storage: StorageMetadata = optumi.metadata.storage;
        return storage.rating[1];
    }
    
    private async saveValue(rating: number) {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const storage: StorageMetadata = optumi.metadata.storage;
        storage.rating = [-1, rating, -1];
        tracker.setMetadata(optumi);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <div style={this.props.style}>
                <Slider
                    getValue={this.getValue}
                    saveValue={this.saveValue}
                    marks={Global.fractionMarks}
                    step={null}
                    label={'DSK'}
                    color={'#68da7c'}
                    styledUnit={FormatUtils.styleRatingUnit()}
                    styledValue={FormatUtils.styleRatingValue()}
                    unstyledValue={FormatUtils.unstyleRatingValue()}
                />
            </div>
        )
    }

    private handleMetadataChange = () => { this.forceUpdate() }

    // Will be called automatically when the component is mounted
	public componentDidMount = () => {
		Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
		Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange);
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

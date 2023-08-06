/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../Global';
import { darken, lighten, Paper } from '@material-ui/core';

interface IProps {
    style?: React.CSSProperties
    children?: JSX.Element | JSX.Element[]
    statusColor: StatusColor | string
    opened: boolean
}

interface IState {}

export enum StatusColor {
    RED = '#f48f8d',
    ORANGE = '#ffab61',
    YELLOW = '#fff21c',
    GREEN = '#68da7c',
    BLUE = '#10A0F9',
    LIGHT_BLUE = '#c3d7ff',
    PURPLE = '#934692',
    DARK_GRAY = '#89858b',
    LIGHT_GRAY = '#e7e5e7'
}

export class StatusWrapper extends React.Component<IProps, IState> {

    private isLightMode: boolean = false;

    constructor(props: IProps) {
        super(props);
        this.isLightMode = Global.themeManager == undefined || Global.themeManager.isLight(Global.themeManager.theme)
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        var color: string;
        if (this.props.statusColor.startsWith('var')) {
            color = getComputedStyle(document.documentElement).getPropertyValue(this.props.statusColor.replace('var(', '').replace(')', '')).trim();
        } else {
            color = this.props.statusColor;
        }

        console.log(color)

        return (
            <div style={this.props.style}>
                <Paper elevation={0} style={{
                    marginLeft: '-6px', 
                    background: this.props.opened ? (this.isLightMode ? darken(color, 0.5) : lighten(color, 0.5)) : color,
                    transition: 'background 750ms cubic-bezier(0.4, 0, 0.2, 1) 0ms',
                }}>
                    <div style={{marginLeft: '6px', padding: '2px'}}>
                        {this.props.children}
                    </div>
                </Paper>
            </div>
        );
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

/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { ServerConnection } from '@jupyterlab/services';
import { PageConfig } from '@jupyterlab/coreutils';
import BreadCrumbs from './BreadCrumbs';
import DirListing from './DirListing';
import { CSSProperties } from '@material-ui/core/styles/withStyles';
import { Global } from '../../../Global';

export interface FileMetadata {
    content: Array<File> | null,
    created: string,
    format: string | null,
    last_modified: string,
    mimetype: string | null,
    name: string,
    path: string,
    size: number | null,
    type: 'notebook' | 'file' | 'directory',
    writable: boolean,
}

interface IProps {
    style?: CSSProperties
    getSelectedFiles: (getSelectedFiles: () => FileMetadata[]) => void
    onAdd?: () => void
}

interface IState {
    serverRoot: string,
    root: FileMetadata,
    path: FileMetadata[],
    files: FileMetadata[],
}

export default class FileBrowser extends React.Component<IProps, IState> {
    private _isMounted = false
    private oldOpen: (event: MouseEvent) => boolean

    private getSelected: () => FileMetadata[]

    constructor(props: IProps) {
        super(props)
        this.props.getSelectedFiles(this.getSelectedFiles)
        this.state = {
            serverRoot: PageConfig.getOption('serverRoot'),
            root: undefined,
            path: [],
            files: [],
        }
    }

    private getSelectedFiles = (): FileMetadata[] => {
        return this.getSelected();
    }

    public request = async (path: string) => {
        const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + 'api' + path;
		return ServerConnection.makeRequest(url, {}, settings).then(response => {
			if (response.status !== 200) throw new ServerConnection.ResponseError(response);
			return response.json();
		})
    }

    private handleOpen = (file: FileMetadata) => {
        if (file.type === 'directory') {
            this.request('/contents/' + file.path).then(json => {
                const newPath = this.state.path
                const depth = file.path.replace(/[^/]/g, '').length
                while (newPath.length > depth) newPath.pop();
                if (file !== this.state.root) newPath.push(file)
                this.safeSetState({
                    path: newPath,
                    files: json.content,
                })
            })
        } else {
            if (this.props.onAdd) this.props.onAdd();
        }
    }

    public render = (): JSX.Element => {
		if (Global.shouldLogOnRender) console.log('ComponentRender (' + new Date().getSeconds() + ')');
        return (
            <div className='jp-FileBrowser' style={this.props.style}>
                <BreadCrumbs serverRoot={this.state.serverRoot} root={this.state.root} path={this.state.path} onOpen={this.handleOpen} />
                <DirListing
                    files={this.state.files}
                    onOpen={this.handleOpen}
                    getSelected={getSelected => this.getSelected = getSelected}
                />
            </div>
        )
    }

    public componentDidMount = () => {
        this._isMounted = true
        this.request('/contents').then(json => {
            this.safeSetState({root: json, files: json.content});
        })
        // Override the JupyterLab context menu open (disable it)
        this.oldOpen = Global.lab.contextMenu.open;
        Global.lab.contextMenu.open = () => false;
    }

    // Add context menu items back
    public componentWillUnmount = () => {
        // Restore the old JupyterLab context menu open
        Global.lab.contextMenu.open = this.oldOpen;
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


























































































// // Copyright (c) Jupyter Development Team.
// // Distributed under the terms of the Modified BSD License.

// import { PageConfig, URLExt } from '@jupyterlab/coreutils';
// (window as any).__webpack_public_path__ = URLExt.join(
//     PageConfig.getBaseUrl(),
//     'example/'
// );

// import '@jupyterlab/application/style/index.css';
// import '@jupyterlab/codemirror/style/index.css';
// import '@jupyterlab/filebrowser/style/index.css';
// import '@jupyterlab/theme-light-extension/style/index.css';
// import '../index.css';

// import { each } from '@lumino/algorithm';

// import { CommandRegistry } from '@lumino/commands';

// import { DockPanel, Menu, SplitPanel, Widget } from '@lumino/widgets';
// import {  } from '@jupyter-widgets/html-manager';

// import { ServiceManager } from '@jupyterlab/services';

// import { Dialog, ToolbarButton, showDialog } from '@jupyterlab/apputils';

// import {
//     CodeMirrorEditorFactory,
//     CodeMirrorMimeTypeService
// } from '@jupyterlab/codemirror';

// import { DocumentManager } from '@jupyterlab/docmanager';

// import { DocumentRegistry } from '@jupyterlab/docregistry';

// import { FileBrowser, FilterFileBrowserModel } from '@jupyterlab/filebrowser';

// import { FileEditorFactory } from '@jupyterlab/fileeditor';

// import {
//     ITranslator,
//     nullTranslator,
//     TranslationManager
// } from '@jupyterlab/translation';

// import { addIcon } from '@jupyterlab/ui-components';

// const LANG = 'en';

// async function main(): Promise<void> {
//     // init translator
//     const translator = new TranslationManager();
//     await translator.fetch(LANG);

//     const manager = new ServiceManager();
//     void manager.ready.then(() => {
//         createApp(manager, translator);
//     });
// }

// function createApp(
//     manager: ServiceManager.IManager,
//     translator?: ITranslator
// ): void {
//     translator = translator || nullTranslator;
//     const trans = translator.load('jupyterlab');

//     const widgets: Widget[] = [];
//     let activeWidget: Widget;

//     const opener = {
//         open: (widget: Widget) => {
//             if (widgets.indexOf(widget) === -1) {
//                 dock.addWidget(widget, { mode: 'tab-after' });
//                 widgets.push(widget);
//             }
//             dock.activateWidget(widget);
//             activeWidget = widget;
//             widget.disposed.connect((w: Widget) => {
//                 const index = widgets.indexOf(w);
//                 widgets.splice(index, 1);
//             });
//         }
//     };

//     const docRegistry = new DocumentRegistry();
//     const docManager = new DocumentManager({
//         registry: docRegistry,
//         manager,
//         opener
//     });
//     const editorServices = {
//         factoryService: new CodeMirrorEditorFactory(),
//         mimeTypeService: new CodeMirrorMimeTypeService()
//     };
//     const wFactory = new FileEditorFactory({
//         editorServices,
//         factoryOptions: {
//             name: trans.__('Editor'),
//             modelName: 'text',
//             fileTypes: ['*'],
//             defaultFor: ['*'],
//             preferKernel: false,
//             canStartKernel: true
//         }
//     });
//     docRegistry.addWidgetFactory(wFactory);

//     const commands = new CommandRegistry();

//     const fbModel = new FilterFileBrowserModel({
//         manager: docManager
//     });
//     const fbWidget = new FileBrowser({
//         id: 'filebrowser',
//         model: fbModel
//     });

//     // Add a creator toolbar item.
//     const creator = new ToolbarButton({
//         icon: addIcon,
//         onClick: () => {
//             void docManager
//                 .newUntitled({
//                     type: 'file',
//                     path: fbModel.path
//                 })
//                 .then(model => {
//                     docManager.open(model.path);
//                 });
//         }
//     });
//     fbWidget.toolbar.insertItem(0, 'create', creator);

//     const panel = new SplitPanel();
//     panel.id = 'main';
//     panel.addWidget(fbWidget);
//     SplitPanel.setStretch(fbWidget, 0);
//     const dock = new DockPanel();
//     panel.addWidget(dock);
//     SplitPanel.setStretch(dock, 1);
//     dock.spacing = 8;

//     document.addEventListener('focus', event => {
//         for (let i = 0; i < widgets.length; i++) {
//             const widget = widgets[i];
//             if (widget.node.contains(event.target as HTMLElement)) {
//                 activeWidget = widget;
//                 break;
//             }
//         }
//     });

//     // Add commands.
//     commands.addCommand('file-open', {
//         label: trans.__('Open'),
//         icon: 'fa fa-folder-open-o',
//         mnemonic: 0,
//         execute: () => {
//             each(fbWidget.selectedItems(), item => {
//                 docManager.openOrReveal(item.path);
//             });
//         }
//     });
//     commands.addCommand('file-rename', {
//         label: trans.__('Rename'),
//         icon: 'fa fa-edit',
//         mnemonic: 0,
//         execute: () => {
//             return fbWidget.rename();
//         }
//     });
//     commands.addCommand('file-save', {
//         execute: () => {
//             const context = docManager.contextForWidget(activeWidget);
//             return context?.save();
//         }
//     });
//     commands.addCommand('file-cut', {
//         label: trans.__('Cut'),
//         icon: 'fa fa-cut',
//         execute: () => {
//             fbWidget.cut();
//         }
//     });
//     commands.addCommand('file-copy', {
//         label: trans.__('Copy'),
//         icon: 'fa fa-copy',
//         mnemonic: 0,
//         execute: () => {
//             fbWidget.copy();
//         }
//     });
//     commands.addCommand('file-delete', {
//         label: trans.__('Delete'),
//         icon: 'fa fa-remove',
//         mnemonic: 0,
//         execute: () => {
//             return fbWidget.delete();
//         }
//     });
//     commands.addCommand('file-duplicate', {
//         label: trans.__('Duplicate'),
//         icon: 'fa fa-copy',
//         mnemonic: 0,
//         execute: () => {
//             return fbWidget.duplicate();
//         }
//     });
//     commands.addCommand('file-paste', {
//         label: trans.__('Paste'),
//         icon: 'fa fa-paste',
//         mnemonic: 0,
//         execute: () => {
//             return fbWidget.paste();
//         }
//     });
//     commands.addCommand('file-download', {
//         label: trans.__('Download'),
//         icon: 'fa fa-download',
//         execute: () => {
//             return fbWidget.download();
//         }
//     });
//     commands.addCommand('file-shutdown-kernel', {
//         label: trans.__('Shut Down Kernel'),
//         icon: 'fa fa-stop-circle-o',
//         execute: () => {
//             return fbWidget.shutdownKernels();
//         }
//     });
//     commands.addCommand('file-dialog-demo', {
//         label: trans.__('Dialog Demo'),
//         execute: () => {
//             dialogDemo();
//         }
//     });
//     commands.addCommand('file-info-demo', {
//         label: trans.__('Info Demo'),
//         execute: () => {
//             const msg = 'The quick brown fox jumped over the lazy dog';
//             void showDialog({
//                 title: 'Cool Title',
//                 body: msg,
//                 buttons: [Dialog.okButton()]
//             });
//         }
//     });

//     commands.addKeyBinding({
//         keys: ['Enter'],
//         selector: '.jp-DirListing',
//         command: 'file-open'
//     });
//     commands.addKeyBinding({
//         keys: ['Accel S'],
//         selector: '.jp-CodeMirrorEditor',
//         command: 'file-save'
//     });
//     window.addEventListener('keydown', event => {
//         commands.processKeydownEvent(event);
//     });

//     // Create a context menu.
//     const menu = new Menu({ commands });
//     menu.addItem({ command: 'file-open' });
//     menu.addItem({ command: 'file-rename' });
//     menu.addItem({ command: 'file-remove' });
//     menu.addItem({ command: 'file-duplicate' });
//     menu.addItem({ command: 'file-delete' });
//     menu.addItem({ command: 'file-cut' });
//     menu.addItem({ command: 'file-copy' });
//     menu.addItem({ command: 'file-paste' });
//     menu.addItem({ command: 'file-shutdown-kernel' });
//     menu.addItem({ command: 'file-dialog-demo' });
//     menu.addItem({ command: 'file-info-demo' });

//     // Add a context menu to the dir listing.
//     // const node = fbWidget.node.getElementsByClassName('jp-DirListing-content')[0];
//     // node.addEventListener('contextmenu', (event: MouseEvent) => {
//     //     event.preventDefault();
//     //     const x = event.clientX;
//     //     const y = event.clientY;
//     //     menu.open(x, y);
//     // });

//     // Attach the panel to the DOM.
//     Widget.attach(panel, document.body);

//     // Handle resize events.
//     window.addEventListener('resize', () => {
//         panel.update();
//     });

//     console.debug('Example started!');
// }

// /**
//  * Create a non-functional dialog demo.
//  */
// function dialogDemo(): void {
//     const body = document.createElement('div');
//     const input = document.createElement('input');
//     input.value = 'Untitled.ipynb';
//     const selector = document.createElement('select');
//     const option0 = document.createElement('option');
//     option0.value = 'python';
//     option0.text = 'Python 3';
//     selector.appendChild(option0);
//     const option1 = document.createElement('option');
//     option1.value = 'julia';
//     option1.text = 'Julia';
//     selector.appendChild(option1);
//     body.appendChild(input);
//     body.appendChild(selector);
//     void showDialog({
//         title: 'Create new notebook'
//     });
// }

// window.addEventListener('load', main);

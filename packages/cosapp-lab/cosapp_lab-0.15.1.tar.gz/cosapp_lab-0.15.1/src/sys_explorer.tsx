// Copyright (c) CoSApp Team
import '../style/sys_exp.css';

import { BoxModel, VBoxView } from '@jupyter-widgets/controls';
import { ILabShell } from '@jupyterlab/application';
import { ReactWidget } from '@jupyterlab/apputils';
import { INotebookTracker } from '@jupyterlab/notebook';
import { Kernel } from '@jupyterlab/services';
import { UUID } from '@lumino/coreutils';
import * as React from 'react';
import { Provider } from 'react-redux';
import { applyMiddleware, compose, createStore } from 'redux';
import thunk from 'redux-thunk';

import { initialState, rootReducer } from './sys_explorer_react/redux/reducers';
import { StateInterface } from './sys_explorer_react/redux/types';
import SysExpUI from './sys_explorer_react/sys_exp_ui';
import { MODULE_NAME, MODULE_VERSION } from './version';

// import { IClientSession } from '@jupyterlab/apputils';
const getEnhancers = () => {
  let enhancers = applyMiddleware(thunk);
  if (
    (window as any).__REDUX_DEVTOOLS_EXTENSION__ &&
    process.env.NODE_ENV === 'development'
  ) {
    enhancers = compose(
      enhancers,
      (window as any).__REDUX_DEVTOOLS_EXTENSION__()
    );
  }
  return enhancers;
};

export class SysExplorerModel extends BoxModel {
  defaults():void {
    return {
      ...super.defaults(),
      _model_name: SysExplorerModel.model_name,
      _model_module: SysExplorerModel.model_module,
      _model_module_version: SysExplorerModel.model_module_version,
      _view_name: SysExplorerModel.view_name,
      _view_module: SysExplorerModel.view_module,
      _view_module_version: SysExplorerModel.view_module_version,
      title: `SysExplorer ${SysExplorerModel.view_module_version}`,
      anchor: 'tab-after',
      system_data: { key: 'None' },
      system_dict: { key: 'None' },
      geo_data: {},
      progress_geo_update: {},
      update_signal: 0,
      notification_msg: { update: 0, msg: '', log: '' },
      server_msg: { update: 0, msg: '', log: '' },
      initial_store: {},
      system_config: {}
    };
  }

  initialize(
    attributes: any,
    options: {
      model_id: string;
      comm?: any;
      widget_manager: any;
    }
  ):void {
    super.initialize(attributes, options);
    this.widget_manager.display_model(undefined as any, this, {});
  }
  static model_name = 'SysExplorerModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'SysExplorerView';
  static view_module = MODULE_NAME;
  static view_module_version = MODULE_VERSION;
}

class WrapperWidget extends ReactWidget {
  _store: any;
  _send_msg: any;
  _model: SysExplorerModel;

  constructor(store: any, send_msg: any, model: SysExplorerModel) {
    super();
    this._store = store;
    this._send_msg = send_msg;
    this._model = model;
  }

  onResize = (msg: any) => {
    window.dispatchEvent(new Event('resize'));
  };

  render() {
    return (
      <Provider store={this._store}>
        <SysExpUI send_msg={this._send_msg} model={this._model} />
      </Provider>
    );
  }
}

export class SysExplorerView extends VBoxView {
  class_name = 'cosapp-sys-explorer';
  /**
   * Notebook tracker to link lifecycle of the view with the related notebook
   */
  static tracker: INotebookTracker;
  /**
   * Application shell to use for inserting the sidecar panel
   */
  static shell: ILabShell;

  /**
   * Public constructor
   */
  initialize(parameters: any): void {
    super.initialize(parameters);
    const nb = SysExplorerView.tracker.currentWidget;
    if (nb) {
      const session = nb.sessionContext.session;
      if (session) {
        session.statusChanged.connect(this._handleKernelStatusChanged, this);
      }
    }
  }

  /**
   * Handle dispose of the parent
   */
  protected _handleKernelStatusChanged(
    sender: any,
    status: Kernel.Status
  ): void {
    if (status === 'restarting' || status === 'dead') {
      sender.statusChanged.disconnect(this._handleKernelStatusChanged, this);
      this.remove();
    }
  }

  getStore(): StateInterface {
    const store = { ...initialState };
    const graphData = this.model.get('system_data');

    const newStore: StateInterface = {
      ...store,
      systemArch: {
        ...store.systemArch,
        systemGraph: graphData.systemGraph,
        systemTree: {
          ...store.systemArch.systemTree,
          nodeData: graphData.systemTree
        },
        systemPBS: graphData.systemPBS
      },
      dashboardState: {
        ...store.dashboardState,
        variableData: graphData.variableData
      }
    };

    const savedStore = this.model.get('initial_store');
    for (const key in savedStore) {
      if (savedStore.hasOwnProperty(key) && newStore.hasOwnProperty(key)) {
        newStore[key] = savedStore[key];
      }
    }
    return newStore;
  }

  store = createStore(rootReducer, this.getStore(), getEnhancers());
  /**
   * Render this view
   */
  render() {
    super.render();
    if (SysExplorerView.shell) {
      const w = this.pWidget;

      // const content = ReactWidget.create(
      //   <Provider store={this.store}>
      //     <SysExpUI send_msg={this.send.bind(this)} model={this.model} />
      //   </Provider>
      // );
      const content = new WrapperWidget(
        this.store,
        this.send.bind(this),
        this.model
      );
      w.addWidget(content);
      w.addClass(this.class_name);
      w.addClass('cosapp-explorer');

      w.title.label = this.model.get('title');
      w.title.closable = true;

      SysExplorerView.shell['_rightHandler'].sideBar.tabCloseRequested.connect(
        (sender: any, tab: any) => {
          tab.title.owner.dispose();
        }
      );
      w.id = UUID.uuid4();
      const anchor = this.model.get('anchor');
      if (anchor === 'right') {
        SysExplorerView.shell.add(w, 'right');
        SysExplorerView.shell.expandRight();
      } else {
        SysExplorerView.shell.add(w, 'main', { mode: anchor });
      }
    }
  }
}

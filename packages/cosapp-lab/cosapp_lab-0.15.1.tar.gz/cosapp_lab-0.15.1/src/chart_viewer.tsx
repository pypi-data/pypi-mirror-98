// Copyright (c) CoSApp Team
import {VBoxView} from '@jupyter-widgets/controls';
import {ILabShell} from '@jupyterlab/application';
import {ReactWidget} from '@jupyterlab/apputils';
import {INotebookTracker} from '@jupyterlab/notebook';
import {Kernel} from '@jupyterlab/services';
import {UUID} from '@lumino/coreutils';
import * as React from 'react';
import {Provider} from 'react-redux';
import {applyMiddleware, compose, createStore} from 'redux';
import thunk from 'redux-thunk';
import '../style/sys_exp.css';
import {ChartViewerModel} from './chart_viewer_model';
import ChartView from './chart_viewer_react/chartview';
import {initialState, rootReducer} from './chart_viewer_react/redux/reducers';
import {StateInterface} from './chart_viewer_react/redux/types';


export const getEnhancers = () => {
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

export const createInitialStore = (store: StateInterface, graphData: any): StateInterface =>
{
  const { recorderData, driverData } = graphData;
  return {
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
      variableData: graphData.variableData,
      portMetaData : graphData.portMetaData,
      computedResult: graphData.computedResult,
      recorderData,
      driverData,
    }
  }
}

class WrapperWidget extends ReactWidget {
  _store: any;
  _send_msg: any;
  _model: ChartViewerModel;

  constructor(store: any, send_msg: any, model: ChartViewerModel) {
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
        <ChartView send_msg={this._send_msg} model={this._model} />
      </Provider>
    );
  }
}

export class ChartViewerView extends VBoxView {
  class_name = 'cosapp-chart-viewer';
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
    const nb = ChartViewerView.tracker.currentWidget;
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

    const newStore: StateInterface = createInitialStore(store, graphData);

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
    if (ChartViewerView.shell) {
      const w = this.pWidget;
      const content = new WrapperWidget(
        this.store,
        this.send.bind(this),
        this.model
      );

      w.addWidget(content);
      w.addClass(this.class_name);
      w.addClass('cosapp-geometry-viewer');

      w.title.label = this.model.get('title');
      w.title.closable = true;

      ChartViewerView.shell['_rightHandler'].sideBar.tabCloseRequested.connect(
        (sender: any, tab: any) => {
          tab.title.owner.dispose();
        }
      );
      w.id = UUID.uuid4();
      const anchor = this.model.get('anchor');
      if (anchor === 'right') {
        ChartViewerView.shell.add(w, 'right');
        ChartViewerView.shell.expandRight();
      } else {
        ChartViewerView.shell.add(w, 'main', { mode: anchor });
      }
    }
  }
}



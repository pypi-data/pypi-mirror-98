// Copyright (c) CoSApp Team
import {BoxModel, VBoxView} from '@jupyter-widgets/controls';
import {ILabShell} from '@jupyterlab/application';
import {ReactWidget} from '@jupyterlab/apputils';
// import { IClientSession } from '@jupyterlab/apputils';
import {INotebookTracker} from '@jupyterlab/notebook';
import {Kernel} from '@jupyterlab/services';
import {UUID} from '@lumino/coreutils';
import * as React from 'react';
import {Provider} from 'react-redux';
import {applyMiddleware, compose, createStore} from 'redux';
import thunk from 'redux-thunk';
import '../style/sys_exp.css';
import GeometryViewWidget from './chart_viewer_react/geometry_view/geometry_view';
import {rootReducer} from './chart_viewer_react/redux/reducers';
import {MODULE_NAME, MODULE_VERSION} from './version';

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

export class GeometryViewerModel extends BoxModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: GeometryViewerModel.model_name,
      _model_module: GeometryViewerModel.model_module,
      _model_module_version: GeometryViewerModel.model_module_version,
      _view_name: GeometryViewerModel.view_name,
      _view_module: GeometryViewerModel.view_module,
      _view_module_version: GeometryViewerModel.view_module_version,
      title: `GeometryViewer ${GeometryViewerModel.view_module_version}`,
      anchor: 'split-right',
      system_data: { key: 'None' },
      geo_data: {},
      progress_geo_update: {},
      update_signal: 0,
      notification_msg: { update: 0, msg: '', log: '' },
      initial_store: {},
    };
  }

  initialize(
    attributes: any,
    options: {
      model_id: string;
      comm?: any;
      widget_manager: any;
    }
  ) {
    super.initialize(attributes, options);
    this.widget_manager.display_model(undefined as any, this, {});
  }
  static model_name = 'GeometryViewerModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'GeometryViewerView';
  static view_module = MODULE_NAME;
  static view_module_version = MODULE_VERSION;
}

export class GeometryViewerView extends VBoxView {
  class_name = 'cosapp-geo-viewer';
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
    const nb = GeometryViewerView.tracker.currentWidget;
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

  store = createStore(rootReducer, getEnhancers());
  /**
   * Render this view
   */
  render() {
    super.render();
    if (GeometryViewerView.shell) {
      const w = this.pWidget;

      const content = ReactWidget.create(
        <Provider store={this.store}>
          <GeometryViewWidget
            send_msg={this.send.bind(this)}
            model={this.model}
          />
        </Provider>
      );
      w.addWidget(content);
      w.addClass(this.class_name);
      w.addClass('cosapp-geometry-viewer');

      w.title.label = this.model.get('title');
      w.title.closable = true;

      GeometryViewerView.shell[
        '_rightHandler'
      ].sideBar.tabCloseRequested.connect((sender: any, tab: any) => {
        tab.title.owner.dispose();
      });
      w.id = UUID.uuid4();
      const anchor = this.model.get('anchor');
      if (anchor === 'right') {
        GeometryViewerView.shell.add(w, 'right');
        GeometryViewerView.shell.expandRight();
      } else {
        GeometryViewerView.shell.add(w, 'main', { mode: anchor });
      }
    }
  }
}

// Copyright (c) CoSApp Team
import {VBoxModel, VBoxView} from '@jupyter-widgets/controls';
import {ILabShell} from '@jupyterlab/application';
import {INotebookTracker} from '@jupyterlab/notebook';
import {Kernel} from '@jupyterlab/services';
import {UUID} from '@lumino/coreutils';
import '../style/sidecar.css';
import {MODULE_NAME, MODULE_VERSION} from './version';




export class SidecarModel extends VBoxModel {
  /**
   * Default properties
   */
  defaults() {
    return {
      ...super.defaults(),
      _model_name: SidecarModel.model_name,
      _model_module: SidecarModel.model_module,
      _model_module_version: SidecarModel.model_module_version,
      _view_name: SidecarModel.view_name,
      _view_module: SidecarModel.view_module,
      _view_module_version: SidecarModel.view_module_version,
      title: 'Sidecar',
      anchor: 'split-right'
    };
  }

  /**
   * Public constructor
   */
  initialize(
    attributes: any,
    options: {
      model_id: string;
      comm?: any;
      widget_manager: any;
    }
  ) {
    super.initialize(attributes, options);
    // Force displaying the element
    this.widget_manager.display_model(undefined as any, this, {});
  }

  static model_name = 'SidecarModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'SidecarView';
  static view_module = MODULE_NAME;
  static view_module_version = MODULE_VERSION;
}

export class SidecarView extends VBoxView {
  /**
   * Notebook tracker to link lifecycle of the view with the related notebook
   */
  static tracker: INotebookTracker;
  /**
   * Application shell to use for inserting the sidecar panel
   */
  static shell: ILabShell;

  class_name = 'cosapp-sidecar';
  /**
   * Public constructor
   */
  initialize(parameters: any): void {
    super.initialize(parameters);
    const nb = SidecarView.tracker.currentWidget;
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

  /**
   * Render this view
   */
  render() {
    super.render();
    if (SidecarView.shell) {
      const w = this.pWidget;
      w.addClass(this.class_name);
      w.addClass('jp-LinkedOutputView');

      w.title.label = this.model.get('title');
      w.title.closable = true;
      // TODO how to make a single left tab closable
      // SidecarView.shell['_leftHandler'].sideBar.tabCloseRequested.connect((sender : any, tab : any) => {
      //     tab.title.owner.dispose();
      // });
      SidecarView.shell['_rightHandler'].sideBar.tabCloseRequested.connect(
        (sender: any, tab: any) => {
          tab.title.owner.dispose();
        }
      );
      w.id = UUID.uuid4();
      const anchor = this.model.get('anchor');
      if (anchor === 'right') {
        SidecarView.shell.add(w, 'right');
        SidecarView.shell.expandRight();
        // } else if(anchor === 'left') {
        //   SidecarView.shell.add(w, "left");
        //   SidecarView.shell.expandLeft();
      } else {
        SidecarView.shell.add(w, 'main', { mode: anchor });
      }
    }
  }
}

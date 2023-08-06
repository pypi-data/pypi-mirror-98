// Copyright (c) CoSApp Team

import {IJupyterWidgetRegistry} from '@jupyter-widgets/base';
import
  {
    ILabShell, JupyterFrontEnd,
    JupyterFrontEndPlugin
  } from '@jupyterlab/application';
import {INotebookTracker} from '@jupyterlab/notebook';
import * as widgetExports from './plugin';
import {MODULE_NAME, MODULE_VERSION} from './version';

const EXTENSION_ID = 'cosapp_lab:plugin';

/**
 * The sidecar plugin.
 */
const sidecarPlugin: JupyterFrontEndPlugin<void> = {
  id: EXTENSION_ID,
  requires: [IJupyterWidgetRegistry, ILabShell],
  optional: [INotebookTracker],
  activate: activateWidgetExtension,
  autoStart: true
};

export default sidecarPlugin;

/**
 * Activate the widget extension.
 */
function activateWidgetExtension(
  app: JupyterFrontEnd,
  registry: IJupyterWidgetRegistry,
  shell: ILabShell,
  tracker: INotebookTracker
): void {
  widgetExports.SysExplorerView.shell = shell;
  widgetExports.SysExplorerView.tracker = tracker;
  widgetExports.GeometryViewerView.shell = shell;
  widgetExports.GeometryViewerView.tracker = tracker;
  widgetExports.ChartViewerView.shell = shell;
  widgetExports.ChartViewerView.tracker = tracker;
  registry.registerWidget({
    name: MODULE_NAME,
    version: MODULE_VERSION,
    exports: widgetExports as any
  });
}

// Copyright (c) CoSApp Team
import { BoxModel } from '@jupyter-widgets/controls';
import { MODULE_NAME, MODULE_VERSION } from './version';

export class ChartViewerModel extends BoxModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: ChartViewerModel.model_name,
      _model_module: ChartViewerModel.model_module,
      _model_module_version: ChartViewerModel.model_module_version,
      _view_name: ChartViewerModel.view_name,
      _view_module: ChartViewerModel.view_module,
      _view_module_version: ChartViewerModel.view_module_version,
      title: `GeometryViewer ${ChartViewerModel.view_module_version}`,
      anchor: 'split-right',
      system_data: { key: 'None' },
      geo_data: {},
      computed_data: {},
      recorder_data: {},
      driver_data: {},
      progress_geo_update: {},
      update_signal: 0,
      notification_msg: { update: 0, msg: '', log: '' },
      initial_store: {},
      chart_template: {},
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
  static model_name = 'ChartViewerModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'ChartViewerView';
  static view_module = MODULE_NAME;
  static view_module_version = MODULE_VERSION;
}

import React, { Component } from 'react';
import { withStyles } from '@material-ui/core';
import { Styles } from '@material-ui/styles/withStyles';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import { SysExplorerModel } from '../../sys_explorer';
import Plot3DView from '../../chart_viewer_react/geometry_view/3dview';
import ControlPanel from './control_panel';
import { StateInterface } from '../redux/types';
import * as ReduxAction from '../redux/actions';
import { connect } from 'react-redux';

/**
 * Selector used to get data from store.
 * @param state
 */
const getThreeData = (state: StateInterface) => {
  return {
    threeData: state.dashboardState.data3D,
    timeStepList: state.dashboardState.timeStepList,
    computingState: state.dashboardState.computing,
    selectedVariable: state.dashboardState.selectedVariable,
  };
};

/**
 *
 *
 * @param {StateInterface} state
 * @returns
 */
const mapStateToProps = (state: StateInterface) => {
  return getThreeData(state);
};

/**
 *
 *
 * @param {(f: any) => void} dispatch
 * @returns
 */
const mapDispatchToProps = (dispatch: (f: any) => void) => {
  return {
    add3DData: (data: any) => dispatch(ReduxAction.dashboardAdd3DData(data)),
    toggleComputing: () => dispatch(ReduxAction.dashboardToggleRun()),
  };
};

const styles: Styles<{}, {}> = () => ({
  root: {
    height: '100%',
    flexGrow: 1,
  },
  paper: {
    background: 'aliceblue',
    height: '100%',
  },
});

interface AppProps {
  send_msg: any;
  model: SysExplorerModel;
  displayStatus: boolean;
  classes: any;
  timeStepList: string[];
  add3DData: any;
  toggleComputing: () => void;
  computingState: boolean;
  selectedVariable: { [key: string]: number };
}

interface AppState {
  threeData: { [key: string]: any };
  logMsg: string;
  updateSignal: number; // Signal to update render
}

/**
 *
 * React component displaying the dashboard panel
 * @class DashBoardView
 * @extends {Component<AppProps, AppState>}
 */
class DashBoardView extends Component<AppProps, AppState> {
  updateInverval: NodeJS.Timeout; // Interval to check current position of object.
  buffer_data: { [key: number]: any };
  time_step: number;
  /**
   * Build a new object.
   *
   * @param props - React properties object. This object should
   * contain the following properties:
   *
   * @param props.model - Current jupyterlab model of widget.
   *
   * @param props.send_msg - Function to send message to backend.
   *
   * @param props.displayStatus - Display status of current panel.
   *
   * @param props.classes - Class for applying style to component.
   * This props is created from `withStyles`.
   *
   * @param props.timeStepList - List of available time steps.
   * This props is mapped from store.
   *
   * @param props.add3DData - Function to dispatch 3D data to redux store.
   * This props is mapped from store.
   *
   * @param props.toggleComputing - Function to toggle computing status in store.
   * This props is mapped from store.
   *
   * @param props.computingState - Current computing state, this props is mapped
   * from store
   *
   * @param props.selectedVariable - List of parameter controllers.
   *
   */
  constructor(props: AppProps) {
    super(props);
    this.props.model.on('change:update_signal', this.computedUpdate);
    this.props.model.on('change:notification_msg', this.updateLog);
    props.model.listenTo(props.model, 'msg:custom', this.on_msg);
    const geo_data = {}; //this.props.model.get("geo_data");
    const step_data = [];
    for (let index = 0; index < Object.keys(geo_data).length; index++) {
      step_data.push('Time step ' + index.toString());
    }
    this.props.add3DData(step_data);

    this.state = { threeData: geo_data, logMsg: '', updateSignal: 1 };
    this.time_step = 0;
    this.buffer_data = {};
  }

  on_msg = (data: any, buffer: any[]) => {
    const threejs_data = data['threejs_data'];
    const binary_position = data['binary_position'];
    const time_step = data['time_step'];

    for (const shape_idx in binary_position) {
      const pos_data = binary_position[shape_idx];
      const face_length = (pos_data[1] - pos_data[0] + 1) / 2;
      for (let idx = 0; idx < face_length; idx++) {
        const vertices = new Float64Array(buffer[pos_data[0] + 2 * idx].buffer);
        const faces = new Uint16Array(buffer[pos_data[0] + 2 * idx + 1].buffer);
        const new_vertices = new Float32Array(vertices.length);
        new_vertices.set(vertices);
        threejs_data[shape_idx][idx]['vertices'] = new_vertices;
        threejs_data[shape_idx][idx]['faces'] = Array.from(faces);
      }
    }
    this.buffer_data[time_step] = threejs_data;
    if ('remaining' in data && data['remaining'] == 0) {
      this.computedUpdate(null, null);
    }
  };

  /**
   *
   * Clear update interval once the component is unmounted.
   * @memberof DashBoardView
   */
  componentWillUnmount = () => {
    clearInterval(this.updateInverval);
  };

  /**
   *
   * Callback of play button, emit a run signal to backend and
   * send a update request each 5 seconds to backend.
   * @memberof DashBoardView
   */
  runBtnHandle = () => {
    if (this.props.computingState) {
      this.printToLog('A driver is running, please wait!');
    } else {
      this.printToLog('Start computing');
      this.setState((prevState: AppState) => ({
        ...prevState,
        threeData: {},
      }));
      this.props.send_msg({
        action: 'runSignal',
        payload: this.props.selectedVariable,
      });
      this.updateInverval = setInterval(() => {
        this.props.send_msg({ action: 'requestUpdate', payload: {} });
      }, 5000);
    }
  };

  /**
   *
   * Helper function used to print message to log window
   * @memberof DashBoardView
   */
  printToLog = (content: string) => {
    const newLog: string =
      this.state.logMsg +
      '\n' +
      '<b>' +
      new Date().toLocaleString() +
      '</b> ' +
      content;
    this.setState((prevState: AppState) => ({ ...prevState, logMsg: newLog }));
  };

  /**
   *
   * This function is called once the computation is finished.
   * Geometry data from backend will be stored to internal state
   * and computing state will be set to `false`
   * @memberof DashBoardView
   */
  computedUpdate = (model, value) => {
    const step_data = [];

    for (let index = 0; index < Object.keys(this.buffer_data).length; index++) {
      step_data.push('Time step ' + index.toString());
    }
    this.props.add3DData(step_data);
    const newLog: string =
      this.state.logMsg +
      '\n' +
      '<b>' +
      new Date().toLocaleString() +
      '</b> ' +
      'Done';
    this.setState(
      (prevState: AppState) => ({
        ...prevState,
        threeData: { ...this.buffer_data },
        logMsg: newLog,
      }),
      () => {
        this.updateRender();
        this.time_step = 0;
        this.buffer_data = {};
      }
    );
    clearInterval(this.updateInverval);
    if (this.props.computingState) {
      this.props.toggleComputing();
    }
  };

  /**
   *
   * Send update signal to `Plot3DView` component.
   * @memberof DashBoardView
   */
  updateRender = () => {
    this.setState((prevState: AppState) => ({
      ...prevState,
      updateSignal: prevState.updateSignal + 1,
    }));
  };

  /**
   *
   * Update log window.
   * @memberof DashBoardView
   */
  updateLog = () => {
    const newMsg: {
      update: number;
      msg: string;
      log: string;
    } = this.props.model.get('notification_msg');

    const newLog: string =
      this.state.logMsg +
      '\n' +
      (newMsg.log !== '' ? newMsg.log + '\n' : '') +
      '<b>' +
      new Date().toLocaleString() +
      '</b> ' +
      newMsg.msg;
    this.setState((prevState: AppState) => ({ ...prevState, logMsg: newLog }));
  };

  render() {
    const { classes } = this.props;
    return (
      <Grid container className={classes.root} spacing={1}>
        <Grid item xs={3}>
          <Paper className={classes.paper}>
            <ControlPanel
              runBtnHandle={this.runBtnHandle}
              logMsg={this.state.logMsg}
            />
          </Paper>
        </Grid>
        <Grid item xs={9} style={{ height: '100%' }}>
          <Paper className={classes.paper}>
            <Plot3DView
              model={this.props.model}
              send_msg={this.props.send_msg}
              displayStatus={this.props.displayStatus}
              threeData={this.state.threeData}
              updateSignal={this.state.updateSignal}
            />
          </Paper>
        </Grid>
      </Grid>
    );
  }
}

export default withStyles(styles)(
  connect(mapStateToProps, mapDispatchToProps)(DashBoardView)
);

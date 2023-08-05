import React, { Component } from 'react';
import { withStyles } from '@material-ui/core';
import { Styles } from '@material-ui/styles/withStyles';
import { StateInterface } from '../redux/types';
import * as ReduxAction from '../redux/actions';
import { Theme } from '@material-ui/core/styles';

import { connect } from 'react-redux';
import Slider from '@material-ui/core/Slider';
import Input from '@material-ui/core/Input';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import DeleteIcon from '@material-ui/icons/Delete';
import IconButton from '@material-ui/core/IconButton';
const styles: Styles<Theme, {}> = (theme: Theme) => ({});

const getVariableList = (state: StateInterface) => {
  return {};
};

const mapStateToProps = (state: StateInterface) => {
  return getVariableList(state);
};

const mapDispatchToProps = (dispatch: (f: any) => void) => {
  return {
    removeParameterController: (variableName: string) =>
      dispatch(ReduxAction.dashboardRemoveController(variableName)),
    updateHandle: (key: string, val: number) =>
      dispatch(ReduxAction.dashboardUpdateController(key, val))
  };
};

interface AppStates {
  value: number;
}

interface AppProps {
  value: number;
  variableName: string;
  classes: any;
  removeParameterController: (varName: string) => void;
  updateHandle: (key: string, val: number) => void;
}

/**
 *
 * React component displaying the variable controller.
 * @class ParameterController
 * @extends {Component<AppProps, AppStates>}
 */
class ParameterController extends Component<AppProps, AppStates> {
  initialVal: number; // Default value of controller.

  /**
   *Creates an instance of ParameterController.
   * @param {AppProps} props
   * @memberof ParameterController
   */
  constructor(props: AppProps) {
    super(props);
    this.initialVal = Number(props.value.toPrecision(3));
    this.state = { value: this.initialVal };
  }

  /**
   *
   *
   * @param {AppProps} oldProps
   * @param {AppStates} oldState
   * @memberof ParameterController
   */
  componentDidUpdate(oldProps: AppProps, oldState: AppStates) {
    if (this.state.value !== oldState.value) {
    }
  }

  /**
   *
   *
   * @memberof ParameterController
   */
  handleSliderChange = (event: any, newValue: number) => {
    const newVal = Number(newValue.toPrecision(3));
    this.setState({
      value:
        Math.abs(newVal) < 0.00001 ? Number(newVal.toExponential()) : newVal
    });
  };

  /**
   *
   *
   * @memberof ParameterController
   */
  handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    this.setState(
      {
        value: event.target.value === '' ? 0 : Number(event.target.value)
      },
      () => {
        this.props.updateHandle(this.props.variableName, this.state.value);
      }
    );
  };

  render() {
    return (
      <div
        style={{
          padding: '10px 10px 10px 10px',
          borderBottom: 'solid 0.5px black'
        }}
      >
        <Typography>{this.props.variableName}</Typography>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={7}>
            <Slider
              min={Math.min(0.1 * this.initialVal, 5 * this.initialVal) - 1}
              max={Math.max(0.1 * this.initialVal, 5 * this.initialVal) + 1}
              step={Math.max(Math.abs(0.05 * this.initialVal), 0.05)}
              value={this.state.value}
              onChange={this.handleSliderChange}
              onChangeCommitted={() => {
                this.props.updateHandle(
                  this.props.variableName,
                  this.state.value
                );
              }}
              aria-labelledby="input-slider"
            />
          </Grid>
          <Grid item xs={3}>
            <Input
              value={this.state.value}
              margin="dense"
              onChange={this.handleInputChange}
              inputProps={{
                step: Math.max(Math.abs(0.05 * this.initialVal), 0.05),
                min: Math.min(0.1 * this.initialVal, 5 * this.initialVal) - 1,
                max: Math.max(0.1 * this.initialVal, 5 * this.initialVal) + 1,
                type: 'number',
                'aria-labelledby': 'input-slider'
              }}
            />
          </Grid>
          <Grid item xs={2}>
            <IconButton
              aria-label="delete"
              onClick={() => {
                this.props.removeParameterController(this.props.variableName);
              }}
            >
              <DeleteIcon fontSize="small" />
            </IconButton>
          </Grid>
        </Grid>
      </div>
    );
  }
}

export default withStyles(styles)(
  connect(mapStateToProps, mapDispatchToProps)(ParameterController)
);

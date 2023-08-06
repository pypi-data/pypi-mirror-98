import React, { Component } from 'react';
import { withStyles } from '@material-ui/core';
import { Styles } from '@material-ui/styles/withStyles';
import { StateInterface } from '../redux/types';
import * as ReduxAction from '../redux/actions';
import { Theme } from '@material-ui/core/styles';
import { connect } from 'react-redux';
import IconButton from '@material-ui/core/IconButton';
import SaveOutlinedIcon from '@material-ui/icons/SaveOutlined';

const styles: Styles<Theme, {}> = (theme: Theme) => ({});

const getVariableList = (state: StateInterface) => {
  return { storeData: state };
};

const mapStateToProps = (state: StateInterface) => {
  return getVariableList(state);
};

const mapDispatchToProps = (dispatch: (f: any) => void) => {
  return {
    sendSaveSignal: () => dispatch(ReduxAction.saveState())
  };
};

interface AppStates {}

interface AppProps {
  classes: any;
  storeData: StateInterface;
  sendSaveSignal: () => void;
}

/**
 *
 * React component displaying save state button.
 * @class SaveStateComponent
 * @extends {Component<AppProps, AppStates>}
 */
class SaveStateComponent extends Component<AppProps, AppStates> {
  /**
   *Creates an instance of SaveStateComponent.
   * @param {AppProps} props
   * @memberof SaveStateComponent
   */
  constructor(props: AppProps) {
    super(props);
  }

  /**
   *
   * Save store data as a json file
   * @memberof SaveStateComponent
   */
  saveStateToJson = () => {
    this.props.sendSaveSignal();
  };
  render() {
    return (
      <IconButton color="inherit" onClick={this.saveStateToJson}>
        <SaveOutlinedIcon />
      </IconButton>
    );
  }
}

export default withStyles(styles)(
  connect(mapStateToProps, mapDispatchToProps)(SaveStateComponent)
);

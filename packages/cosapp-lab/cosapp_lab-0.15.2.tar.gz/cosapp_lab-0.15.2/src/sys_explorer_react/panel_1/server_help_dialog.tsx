import React, { Component } from 'react';
import Button from '@material-ui/core/Button';

import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
import { Theme } from '@material-ui/core/styles';
import { Styles } from '@material-ui/styles/withStyles';
import { withStyles } from '@material-ui/core';
interface AppProps {
  open: boolean;
  switchFunction: () => void;
}
interface AppState {
  open: boolean;
}

const styles: Styles<Theme, {}> = (theme: Theme) => ({});

export class ServerHelpDialog extends Component<AppProps, AppState> {
  /**
   *
   *
   * @returns
   * @memberof ServerHelpDialog
   */
  render() {
    return (
      <div>
        <Dialog
          keepMounted={false}
          open={this.props.open}
          aria-labelledby="form-dialog-title"
          fullWidth={true}
          maxWidth="sm"
        >
          <DialogTitle>{'CosApp server help'}</DialogTitle>
          <DialogContent>
            <p>
              CosApp server allow user to share their CosApp system instance
              with other outside notebook environement.
            </p>
            <p>
              Once the server is started with <strong>START SERVER</strong>{' '}
              button, server access information is shown in the server log :
              address of server (<strong>BASE_URL</strong>) and user access
              token (<strong>USER_TOKEN</strong>). Other user need to have these
              information in order to connect to current CosApp instance. There
              are two API for interacting with a system:
            </p>
            <br />
            <p>
              Get system information
              <ul>
                <li> Method : POST </li>
                <li>
                  {' '}
                  Address : <strong>BASE_URL</strong>/cosapp/server/info{' '}
                </li>
                <li>
                  {' '}
                  Request body : {'{"token": '}
                  <strong>USER_TOKEN</strong>
                  {'}'}{' '}
                </li>
                <li>
                  {' '}
                  Success response :{' '}
                  {
                    '{"children_list": List, "children_port" : Dict, "children_drive" : Dict}'
                  }{' '}
                </li>
                <li> Error response : -1 </li>
              </ul>
            </p>
            <p></p>
            <p>
              Run system with new parameters
              <ul>
                <li> Method : POST </li>
                <li>
                  {' '}
                  Address : <strong>BASE_URL</strong>/cosapp/server/run{' '}
                </li>
                <li>
                  {' '}
                  Request body : {'{"token": '}
                  <strong>USER_TOKEN</strong>
                  {', "data" :{"parameters" : Dict, "result" : List}} '}{' '}
                </li>
                <li>
                  {' '}
                  Success response :{' '}
                  {'{"error": None, "result" : Dict, "log" : string}'}{' '}
                </li>
                <li>
                  {' '}
                  Error response :{' '}
                  {'{"error": List", "result" : None, "log" : None}'}{' '}
                </li>
              </ul>
            </p>
          </DialogContent>
          <DialogActions>
            <Button
              variant="contained"
              color="primary"
              onClick={this.props.switchFunction}
            >
              Close
            </Button>
          </DialogActions>
        </Dialog>
      </div>
    );
  }
}

export default withStyles(styles)(ServerHelpDialog);

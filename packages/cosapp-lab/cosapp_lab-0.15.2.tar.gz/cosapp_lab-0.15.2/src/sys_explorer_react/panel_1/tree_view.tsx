import { withStyles } from '@material-ui/core';
import Accordion from '@material-ui/core/Accordion';
import AccordionDetails from '@material-ui/core/AccordionDetails';
import AccordionSummary from '@material-ui/core/AccordionSummary';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import { fade, Theme } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import AddCircleOutlineIcon from '@material-ui/icons/AddCircleOutline';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import RemoveCircleOutlineIcon from '@material-ui/icons/RemoveCircleOutline';
import VisibilityIcon from '@material-ui/icons/Visibility';
import { Styles } from '@material-ui/styles/withStyles';
import React, { Component } from 'react';
import { connect } from 'react-redux';
import SortableTree from 'react-sortable-tree';
import 'react-sortable-tree/style.css';
import { SysExplorerModel } from '../../sys_explorer';
import * as ReduxAction from '../redux/actions';
import { getNodeFullPath, updateNodeId } from '../redux/tools';
import { StateInterface } from '../redux/types';
import { AddSystemDialog } from './new_system_dialog';
import ServerHelpDialog from './server_help_dialog';
import PortEditor from './port_editor_dialog';

const styles: Styles<Theme, {}> = (theme: Theme) => ({
  mainPanel: {
    height: '100%',
    width: '100%',
    display: 'flex',
    flexDirection: 'column'
  },
  topPanel: {
    width: '100%',
    flex: '1 1 auto'
  },
  bottomPanel: {
    height: 'auto',
    width: '100%'
  },
  grow: {
    flexGrow: 1
  },
  menuButton: {
    marginRight: theme.spacing(2)
  },
  title: {
    display: 'none',
    [theme.breakpoints.up('sm')]: {
      display: 'block'
    }
  },
  search: {
    position: 'relative',
    borderRadius: theme.shape.borderRadius,
    backgroundColor: fade(theme.palette.common.white, 0.15),
    '&:hover': {
      backgroundColor: fade(theme.palette.common.white, 0.25)
    },
    marginRight: 0,
    marginLeft: 0,
    width: '100%',
    [theme.breakpoints.up('sm')]: {
      marginLeft: 0,
      width: 'auto'
    }
  },
  searchIcon: {
    width: theme.spacing(7),
    height: '100%',
    position: 'absolute',
    pointerEvents: 'none',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  },
  inputRoot: {
    color: 'inherit'
  },
  inputInput: {
    padding: theme.spacing(1, 1, 1, 7),
    transition: theme.transitions.create('width'),
    width: '100%',
    [theme.breakpoints.up('md')]: {
      width: 200
    }
  },
  treeNode: {
    '& .rst__rowContents': {
      minWidth: '120px',
      backgroundColor: 'seashell'
    }
  },
  summaryExpandIcon: {
    padding: 0
  },
  summaryContent: {
    margin: '7px 0!important'
  },
  summaryRoot: {
    minHeight: 36,
    margin: '16px 0 0 0',
    background: '#d5d4d2'
  },
  summaryExpanded: {
    minHeight: '24px!important'
  },
  panelRoot: {
    height: 150,
    overflowY: 'auto',
    marginBottom: 10
  }
});

interface AppState {
  newSystemDialog: boolean;
  activatedTreeNode: { [key: string]: boolean };
  currentNodeData: { node: any; path: any };
  treeNodeResetSignal: number;
  expandNotification: boolean;
  serverToken: string;
  serverLog: string;
  helpDialog: boolean;
  portEditorState: boolean;
}

interface AppProps {
  systemConfig: { [key: string]: any };
  send_msg: any;
  model: SysExplorerModel;
  classes: any;
  treeData: any;
  graphPosition: {
    [key: string]: { visible: boolean; position: Array<number> };
  };
  selectedNode: string;
  treeDataChanged: (treeData: any, updatePbs?: boolean) => void;
  removeTreeNode: (node: any, path: any) => void;
  lockGraph: (status: boolean) => void;
  updateFilter: (data: Array<string>, selected: Array<string>) => void;
  saveGraphPosition: (data: {
    [key: string]: { visible: boolean; position: Array<number> };
  }) => void;
  updateConnectionGraph: (
    data: { [key: string]: string },
    root: string
  ) => void;

  updateSelectedNode: (nodeId: string) => void;
}

const getTreeData = (state: StateInterface) => {
  return {
    treeData: state.systemArch.systemTree.nodeData,
    systemConfig: state.systemConfig,
    graphPosition: state.systemArch.systemPBS,
    selectedNode: state.systemArch.systemTree.selectedNode
  };
};

const mapStateToProps = (state: StateInterface) => {
  return getTreeData(state);
};

const mapDispatchToProps = (dispatch: (f: any) => void) => {
  return {
    treeDataChanged: (treeData: any, updatePbs = false) =>
      dispatch(ReduxAction.archUpdateTreeData(treeData, updatePbs)),

    removeTreeNode: (node: any, path: any) =>
      dispatch(ReduxAction.archRemoveNode(node, path)),

    lockGraph: (status: boolean) => dispatch(ReduxAction.archLockGraph(status)),

    updateFilter: (data: Array<string>, selected: Array<string>) =>
      dispatch(ReduxAction.archFilterNode(data, selected)),

    saveGraphPosition: (data: {
      [key: string]: { visible: boolean; position: Array<number> };
    }) => dispatch(ReduxAction.archSaveGraphPosition(data)),

    updateConnectionGraph: (data: { [key: string]: string }, root: string) =>
      dispatch(ReduxAction.archUpdateConnectionGraph(data, root)),

    updateSelectedNode: (nodeId: string) =>
      dispatch(ReduxAction.archSelectNode(nodeId))
  };
};

export class TreePanel extends Component<AppProps, AppState> {
  private currentURL: string;

  constructor(props: AppProps) {
    super(props);
    this.state = {
      newSystemDialog: false,
      currentNodeData: { node: null, path: null },
      activatedTreeNode: {},
      treeNodeResetSignal: 0,
      expandNotification: false,
      serverToken: '',
      serverLog: 'Starting server, please wait...',
      helpDialog: false,
      portEditorState: false
    };

    this.currentURL = this.getCurrentUrl();
    this.props.model.on('change:server_msg', this.updateServerLog, this);
  }

  private getCurrentUrl = () => {
    const currentUrl = window.location.origin;
    let postfix = '/';
    if (typeof document !== 'undefined' && document) {
      const el = document.getElementById('jupyter-config-data');
      let configData: { [key: string]: string };
      if (el) {
        configData = JSON.parse(el.textContent || '');
        postfix = configData['baseUrl'];
      }
    }

    return currentUrl + postfix;
  };

  closeNewSystemDialog = () => {
    this.props.lockGraph(false);
    this.setState(state => {
      return { ...state, newSystemDialog: false };
    });
  };

  switchHelpDialog = () => {
    this.setState(preState => ({
      ...preState,
      helpDialog: !preState.helpDialog
    }));
  };

  filterView = () => {
    const allNode = Object.keys(this.state.activatedTreeNode);
    const activatedNode = allNode.filter(
      key => this.state.activatedTreeNode[key]
    );

    const selectedNode = [];
    activatedNode.forEach(nodeName => {
      selectedNode.push(nodeName);
      const path = nodeName.split('.');
      for (let idx = 1; idx < path.length; idx++) {
        const newNode = path.slice(0, idx).join('.');
        if (!selectedNode.includes(newNode)) {
          selectedNode.push(newNode);
        }
      }
    });

    if (selectedNode.length > 0) {
      this.props.updateFilter(selectedNode, activatedNode);
    } else {
      this.props.updateFilter([], []);
    }
  };

  clearFilterView = () => {
    this.props.updateFilter([], []);
    this.setState(oldState => ({
      ...oldState,
      treeNodeResetSignal: oldState.treeNodeResetSignal + 1
    }));
  };

  updateState = (node: any, value: boolean) => {
    this.setState(oldState => {
      const oldActivated = JSON.parse(
        JSON.stringify(oldState.activatedTreeNode)
      );
      oldActivated[node.id] = value;
      return { ...oldState, activatedTreeNode: oldActivated };
    });
  };

  /**
   *
   *
   * @private
   * @memberof TreePanel
   */
  private updateServerLog = (model, value) => {
    let msg: string;
    if (value['msg'] === 'ok') {
      msg = `
      Server is running at ${this.currentURL}
      User token is ${this.state.serverToken}
      `;
    } else if (value['msg'] === 'error') {
      msg = `
      Failed to start server
      Error : ${value['log']}
      `;
    } else if (value['msg'] === 'update') {
      const prevMsg = this.state.serverLog;
      msg = prevMsg + `${value['log']}`;
    }
    this.setState(preState => ({ ...preState, serverLog: msg }));
  };

  /**
   * Send start server to backend and open server log
   * window
   *
   * @memberof TreePanel
   */
  switchServer = (event: React.ChangeEvent<{}>) => {
    const currentMode = this.props.systemConfig.mode;
    if (currentMode === 'edit') {
      alert('Can not start server in editor mode');
      return;
    }
    let token, oldToken;
    if (this.state.serverToken == '') {
      token =
        Math.random()
          .toString(36)
          .substr(2) +
        Math.random()
          .toString(36)
          .substr(2);
      this.setState(
        prevState => ({
          ...prevState,
          expandNotification: !prevState.expandNotification,
          serverToken: token
        }),
        () => {
          this.props.send_msg({
            action: 'switchServer',
            payload: {
              signal: this.state.expandNotification,
              token,
              url: this.currentURL
            }
          });
        }
      );
    } else {
      oldToken = this.state.serverToken;
      this.setState(
        prevState => ({
          ...prevState,
          expandNotification: !prevState.expandNotification,
          serverToken: ''
        }),
        () => {
          this.props.send_msg({
            action: 'switchServer',
            payload: {
              signal: this.state.expandNotification,
              token: oldToken,
              url: this.currentURL
            }
          });
        }
      );
    }
  };

  componentWillUnmount() {
    if (this.state.serverToken != '') {
      const oldToken = this.state.serverToken;
      this.props.send_msg({
        action: 'switchServer',
        payload: { signal: false, token: oldToken, url: this.currentURL }
      });
    }
  }

  switchPortEditor = () => {
    this.setState(oldState => ({
      ...oldState,
      portEditorState: !oldState.portEditorState
    }));
  };

  render() {
    const { classes } = this.props;
    return (
      <div className={classes.mainPanel}>
        <PortEditor
          open={this.state.portEditorState}
          switch={this.switchPortEditor}
        />
        <AddSystemDialog
          open={this.state.newSystemDialog}
          handleClose={this.closeNewSystemDialog}
          nodeData={this.state.currentNodeData}
        />
        <ServerHelpDialog
          switchFunction={this.switchHelpDialog}
          open={this.state.helpDialog}
        />
        <div className={classes.search}>
          {/* <div className={classes.searchIcon}>
            <SearchIcon/>
          </div> */}
          <Button
            style={{ width: '33%' }}
            size="small"
            variant="outlined"
            onClick={this.filterView}
          >
            Filter
          </Button>
          <Button
            style={{ width: '33%' }}
            fullWidth={true}
            size="small"
            variant="outlined"
            onClick={this.clearFilterView}
          >
            Clear
          </Button>
          <Button
            style={{ width: '33%' }}
            fullWidth={true}
            size="small"
            variant="outlined"
            onClick={this.switchPortEditor}
          >
            Port editor
          </Button>
        </div>
        <div className={classes.topPanel}>
          <SortableTree
            canDrag={true}
            treeData={this.props.treeData}
            onChange={this.props.treeDataChanged}
            scaffoldBlockPxWidth={35}
            rowHeight={50}
            generateNodeProps={({ node, path }) => {
              const currentNode = node;
              return {
                buttons: [
                  <ViewButton
                    node={node}
                    path={path}
                    updateState={this.updateState}
                    resetSignal={this.state.treeNodeResetSignal}
                  />,
                  <IconButton
                    // style={{ display: "None" }}
                    onClick={() => {
                      this.props.removeTreeNode(node, path);
                    }}
                    aria-label="remove"
                    size="small"
                    color="secondary"
                  >
                    <RemoveCircleOutlineIcon fontSize="inherit" />
                  </IconButton>,
                  <IconButton
                    // style={{ display: "None" }}
                    onClick={event => {
                      this.props.lockGraph(true);
                      this.setState({
                        newSystemDialog: true,
                        currentNodeData: { node, path }
                      });
                    }}
                    aria-label="add"
                    size="small"
                    color="primary"
                  >
                    <AddCircleOutlineIcon fontSize="inherit" />
                  </IconButton>
                ],
                className: `${classes.treeNode}`,
                onClick: () => {
                  if (currentNode.id === this.props.selectedNode) {
                    this.props.updateSelectedNode(null);
                  } else {
                    this.props.updateSelectedNode(currentNode.id);
                  }
                },
                style:
                  currentNode.id === this.props.selectedNode
                    ? {
                        border: '3px solid blue'
                      }
                    : {}
              };
            }}
            onMoveNode={args => {
              const allNode = Object.keys(this.state.activatedTreeNode);
              const activatedNode = allNode.filter(
                key => this.state.activatedTreeNode[key]
              );
              if (activatedNode.length > 0) {
                this.clearFilterView();
              }

              const { prevPath, path, node, treeData } = args;
              const oldId = node.id;
              const newId = getNodeFullPath(treeData, path as number[]);
              if (oldId == newId) {
                return;
              }
              const updatedNodeId: { [key: string]: string } = updateNodeId(
                treeData,
                oldId,
                newId
              );
              const newActivated = JSON.parse(
                JSON.stringify(this.state.activatedTreeNode)
              );

              for (const [key, value] of Object.entries(updatedNodeId)) {
                if (key in newActivated) {
                  newActivated[value] = newActivated[key];
                  delete newActivated[key];
                }
              }
              this.setState(oldState => ({
                ...oldState,
                activatedTreeNode: newActivated
              }));
              const currentPbs = { ...this.props.graphPosition };

              for (const [key, value] of Object.entries(updatedNodeId)) {
                if (key in currentPbs) {
                  currentPbs[value] = currentPbs[key];
                  delete currentPbs[key];
                }
              }

              this.props.saveGraphPosition(currentPbs);
              this.props.treeDataChanged(treeData, true);
              this.props.updateConnectionGraph(updatedNodeId, oldId);
            }}
          />
        </div>

        <div className={classes.bottomPanel}>
          <Accordion square={false} expanded={this.state.expandNotification}>
            {this.props.systemConfig.mode === 'run' ? (
              <AccordionSummary
                expandIcon={<ExpandMoreIcon />}
                aria-controls="panel1a-content"
                classes={{
                  root: classes.summaryRoot,
                  expanded: classes.summaryExpanded,
                  expandIcon: classes.summaryExpandIcon,
                  content: classes.summaryContent
                }}
              >
                <Button
                  variant="contained"
                  size="small"
                  style={{ minWidth: '121px' }}
                  color={
                    this.state.expandNotification ? 'secondary' : 'primary'
                  }
                  onClick={this.switchServer}
                >
                  {this.state.expandNotification
                    ? 'Stop server'
                    : 'Start server'}
                </Button>
                <div style={{ flexGrow: 1 }}></div>
                <Button
                  variant="contained"
                  size="small"
                  onClick={this.switchHelpDialog}
                >
                  Help
                </Button>
              </AccordionSummary>
            ) : (
              <AccordionSummary
                aria-controls="panel1a-content"
                classes={{
                  root: classes.summaryRoot,
                  expanded: classes.summaryExpanded,
                  expandIcon: classes.summaryExpandIcon,
                  content: classes.summaryContent
                }}
              >
                <Button
                  variant="contained"
                  size="small"
                  style={{ marginRight: '5px', width: '30%' }}
                >
                  Add
                </Button>
                <Button
                  variant="contained"
                  size="small"
                  style={{ marginRight: '5px', width: '30%' }}
                >
                  Edit
                </Button>
                <Button
                  variant="contained"
                  size="small"
                  style={{ marginRight: '5px', width: '30%' }}
                >
                  Remove
                </Button>
              </AccordionSummary>
            )}
            <AccordionDetails classes={{ root: classes.panelRoot }}>
              <Typography style={{ whiteSpace: 'pre-line' }} variant="body2">
                {this.state.serverLog}
              </Typography>
            </AccordionDetails>
          </Accordion>
        </div>
      </div>
    );
  }
}

export class ViewButton extends Component<
  {
    node: any;
    path: any;
    updateState: (node: any, value: boolean) => void;
    resetSignal: number;
  },
  { checked: boolean }
> {
  private _node: any;
  private _path: string[];
  constructor(props) {
    super(props);
    this.props.updateState(this.props.node, false);
    this._node = this.props.node;
    this._path = this.props.path;
    this.state = {
      checked: false
    };
  }

  UNSAFE_componentWillReceiveProps(newProps) {
    const oldId = this._node.id;
    const newId = newProps.node.id;

    if (oldId != newId) {
      this._node = newProps.node;
      this._path = newProps.path;
    }
  }

  componentDidUpdate(prevProps, prevState) {
    if (this.props.resetSignal != prevProps.resetSignal) {
      this.setState(
        oldState => ({ checked: false }),
        () => {
          this.props.updateState(this._node, false);
        }
      );
    }
  }

  render() {
    return (
      <IconButton
        onClick={event => {
          this.setState(
            oldState => ({ checked: !oldState.checked }),
            () => {
              this.props.updateState(this._node, this.state.checked);
            }
          );
        }}
        aria-label="add"
        size="small"
        color={this.state.checked ? 'primary' : 'default'}
      >
        <VisibilityIcon fontSize="inherit" />
      </IconButton>
    );
  }
}

export default withStyles(styles)(
  connect(mapStateToProps, mapDispatchToProps)(TreePanel)
);

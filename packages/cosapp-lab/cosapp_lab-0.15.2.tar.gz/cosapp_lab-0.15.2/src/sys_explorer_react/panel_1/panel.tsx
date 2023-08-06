import * as React from 'react';
import { withStyles } from '@material-ui/core';
import { Styles } from '@material-ui/styles/withStyles';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import TreePanel from './tree_view';
import GraphPanel from './graph_view';
import PBSPanel2 from './pbs_view_2';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import { SysExplorerModel } from '../../sys_explorer';
interface AppState {
  tabValue: number;
}

interface AppProps {
  classes: any;
  send_msg: any;
  model: SysExplorerModel;
}

function a11yProps(index: any) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}

const styles: Styles<{}, {}> = () => ({
  root: {
    height: '100%',
    flexGrow: 1,
  },
  paper: {
    background: 'aliceblue',
    height: '100%',
    display: 'flex',
    flexFlow: 'column',
  },
  tabRoot: {
    minHeight: '25px',
    height: '25px',
    '& button': {
      minHeight: '25px!important',
    },
  },
});

class PanelOne extends React.Component<AppProps, AppState> {
  private tabRef: any;
  private panelRef: React.RefObject<HTMLDivElement>;
  constructor(props: any) {
    super(props);
    this.state = { tabValue: 0 };
    this.tabRef = React.createRef();
    this.panelRef = React.createRef<HTMLDivElement>();
  }

  handleChange = (event: React.ChangeEvent<{}>, newValue: number) => {
    this.setState((old) => ({ ...old, tabValue: newValue }));
  };

  componentDidMount() {
    setTimeout(() => {
      this.tabRef.current.click();
    }, 500);
  }

  render() {
    const { classes } = this.props;
    return (
      <Grid container className={classes.root} spacing={1}>
        <Grid style={{ height: '100%' }} item xs={3}>
          <Paper className={classes.paper}>
            {/* <TreePanel
              send_msg={this.props.send_msg}
              model={this.props.model}
            /> */}
          </Paper>
        </Grid>
        <Grid style={{ height: '100%' }} item xs={9}>
          <Paper className={classes.paper}>
            <Tabs
              classes={{
                root: classes.tabRoot,
              }}
              value={this.state.tabValue}
              onChange={this.handleChange}
              aria-label='simple tabs example'
              variant='fullWidth'>
              <Tab label='PBS view' {...a11yProps(1)} ref={this.tabRef} />
              <Tab label='Connections view' {...a11yProps(0)} />
            </Tabs>
            <div
              id={'simple-tabpanel-0'}
              ref={this.panelRef}
              aria-labelledby={'simple-tab-0'}
              style={
                this.state.tabValue === 0
                  ? { flexGrow: 1, height: 'calc(100% - 25px)' }
                  : {
                      flexGrow: 1,
                      height: 'calc(100% - 25px)',
                      position: 'absolute',
                      left: '-9999px',
                    }
              }>
              <PBSPanel2 signal={this.state.tabValue} />
            </div>
            <div
              id={'simple-tabpanel-1'}
              aria-labelledby={'simple-tab-1'}
              style={
                this.state.tabValue === 1
                  ? { flexGrow: 1, height: 'calc(100% - 25px)' }
                  : {
                      flexGrow: 1,
                      height: 'calc(100% - 25px)',
                      position: 'absolute',
                      left: '-9999px',
                    }
              }>
              <GraphPanel signal={this.state.tabValue} />
            </div>
          </Paper>
        </Grid>
      </Grid>
    );
  }
}

export default withStyles(styles)(PanelOne);

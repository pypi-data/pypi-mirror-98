import * as React from 'react';
import { makeStyles, useTheme } from '@material-ui/core/styles';
import clsx from 'clsx';
import Drawer from '@material-ui/core/Drawer';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import List from '@material-ui/core/List';
import CssBaseline from '@material-ui/core/CssBaseline';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';
import ContactMailOutlinedIcon from '@material-ui/icons/ContactMailOutlined';
import LibraryBooksOutlinedIcon from '@material-ui/icons/LibraryBooksOutlined';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import AccountTreeOutlinedIcon from '@material-ui/icons/AccountTreeOutlined';
import DashboardOutlinedIcon from '@material-ui/icons/DashboardOutlined';
import AssignmentOutlinedIcon from '@material-ui/icons/AssignmentOutlined';
import DeveloperBoardOutlinedIcon from '@material-ui/icons/DeveloperBoardOutlined';
import Tooltip from '@material-ui/core/Tooltip';
import PanelOne from './panel_1/panel';
import { useDispatch, useSelector } from 'react-redux';
import { mainSwitchPanel, resetStore } from './redux/actions';
import DashBoardView from './panel_3/dashboard';
import { StateInterface, PanelStatusInterface } from './redux/types';
import { SysExplorerModel } from '../sys_explorer';
import { withStyles } from '@material-ui/core/styles';
import SaveStateComponent from './toolbar/save_state';

const drawerWidth = 240; // Default width of side menu.

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    height: '100%',
  },
  grow: {
    flexGrow: 1,
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  appBarShift: {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  menuButton: {
    marginRight: 36,
  },
  hide: {
    display: 'none',
  },
  drawer: {
    width: drawerWidth,
    flexShrink: 0,
    whiteSpace: 'nowrap',
  },
  drawerOpen: {
    width: drawerWidth,
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  drawerClose: {
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    overflowX: 'hidden',
    width: theme.spacing(7) + 1,
    [theme.breakpoints.up('sm')]: {
      width: theme.spacing(7) + 1,
    },
  },
  toolbar: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: '0 8px',
    // eslint-disable-next-line
    ['@media (min-width:600px)']: {
      minHeight: '48px',
    },
    ...theme.mixins.toolbar,
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing(3),
  },
}));

interface AppProps {
  send_msg: any; // Function to send message to jupyter backend
  model: SysExplorerModel; // Jupyter widget model.
}

/**
 * Selector to get mainState of store.
 * @param {StateInterface} state - current redux store
 * @return {PanelStatusInterface} - mainState of store
 */
const getPanelState = (state: StateInterface) => {
  return state.mainState;
};

/**
 *
 *
 * @param {StateInterface} state
 * @returns
 */
const getSystemConfig = (state: StateInterface) => {
  return state.systemConfig;
};

/**React component that defines the main interface of widget.
 *
 * @param {AppProps} props - React properties object containing
 * the following properties
 *
 * @param {any} props.send_msg - A void function used to send message to back end.
 *
 * @param {SysExplorerModel} props.model - Jupyter widget model.
 *
 */
const SysExpUI: React.FC<AppProps> = (props) => {
  const classes = useStyles({});
  const theme = useTheme();
  const dispatch = useDispatch();
  const [open, setOpen] = React.useState(false);
  const panelState: PanelStatusInterface = useSelector(getPanelState);
  const systemConfig: { [key: string]: any } = useSelector(getSystemConfig);
  // dispatch(serverGetData(graphData));

  /** Dispatch a request to redux store to switch panel
   * @param text {string} - Name of panel
   */
  function setItemState(text: string) {
    dispatch(mainSwitchPanel(text));
  }

  /** Switch state of drawer
   */
  function handleDrawerOpen() {
    window.dispatchEvent(new Event('resize'));
    setOpen(true);
  }
  /** Switch state of drawer
   */
  function handleDrawerClose() {
    window.dispatchEvent(new Event('resize'));
    setOpen(false);
  }
  /** Reset store to initial value once the component is unmounted
   */
  React.useEffect(() => {
    return () => {
      dispatch(resetStore());
    };
  }, []);

  return (
    <div className={classes.root}>
      <CssBaseline />
      <AppBar
        position='absolute'
        className={clsx(classes.appBar, {
          [classes.appBarShift]: open,
        })}
      >
        <Toolbar variant='dense'>
          <IconButton
            color='inherit'
            aria-label='Open drawer'
            onClick={handleDrawerOpen}
            edge='start'
            className={clsx(classes.menuButton, {
              [classes.hide]: open,
            })}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant='h6' noWrap>
            COSAPP EXPLORE
          </Typography>
          <div className={classes.grow} />
          <SaveStateComponent />
        </Toolbar>
      </AppBar>
      <Drawer
        variant='permanent'
        className={clsx(classes.drawer, {
          [classes.drawerOpen]: open,
          [classes.drawerClose]: !open,
        })}
        classes={{
          paper: clsx({
            [classes.drawerOpen]: open,
            [classes.drawerClose]: !open,
          }),
        }}
        open={open}
      >
        <div className={classes.toolbar}>
          <IconButton onClick={handleDrawerClose}>
            {theme.direction === 'rtl' ? (
              <ChevronRightIcon />
            ) : (
              <ChevronLeftIcon />
            )}
          </IconButton>
        </div>
        <Divider />
        <List>
          {/* **************************************************************** */}
          <ListItem
            className={'hideDiv'}
            button
            key='Project_Overview'
            onClick={() => setItemState('Project_Overview')}
          >
            <Tooltip title='Project overview'>
              <ListItemIcon>
                {!panelState.panel_0[0] ? (
                  <AssignmentOutlinedIcon fontSize='large' color='disabled' />
                ) : (
                  <AssignmentOutlinedIcon fontSize='large' color='primary' />
                )}
              </ListItemIcon>
            </Tooltip>
            <ListItemText primary='Project overview' />
          </ListItem>
          <Divider />
          {/* **************************************************************** */}
          <ListItem
            className={'hideDiv'}
            button
            key='User_Management'
            onClick={() => setItemState('User_Management')}
          >
            <Tooltip title='User management'>
              <ListItemIcon>
                {!panelState.panel_4[0] ? (
                  <ContactMailOutlinedIcon fontSize='large' color='disabled' />
                ) : (
                  <ContactMailOutlinedIcon fontSize='large' color='primary' />
                )}
              </ListItemIcon>
            </Tooltip>
            <ListItemText primary='User management' />
          </ListItem>
          <Divider />
          {/* **************************************************************** */}
          <ListItem
            button
            key='System_Arc'
            onClick={() => setItemState('System_Arc')}
          >
            <Tooltip title='System architecture'>
              <ListItemIcon>
                {!panelState.panel_1[0] ? (
                  <AccountTreeOutlinedIcon fontSize='large' color='disabled' />
                ) : (
                  <AccountTreeOutlinedIcon fontSize='large' color='primary' />
                )}
              </ListItemIcon>
            </Tooltip>
            <ListItemText primary='System architecture' />
          </ListItem>
          <Divider />
          {/* **************************************************************** */}
          <ListItem
            className={'hideDiv'}
            button
            key='Module_Library'
            onClick={() => setItemState('Module_Library')}
          >
            <Tooltip title='Module library'>
              <ListItemIcon>
                {!panelState.panel_5[0] ? (
                  <LibraryBooksOutlinedIcon fontSize='large' color='disabled' />
                ) : (
                  <LibraryBooksOutlinedIcon fontSize='large' color='primary' />
                )}
              </ListItemIcon>
            </Tooltip>
            <ListItemText primary='Module library' />
          </ListItem>
          <Divider />
          {/* **************************************************************** */}
          <ListItem
            className={'hideDiv'}
            button
            key='Module_Creator'
            onClick={() => setItemState('Module_Creator')}
          >
            <Tooltip title='Module creator'>
              <ListItemIcon>
                {!panelState.panel_2[0] ? (
                  <DeveloperBoardOutlinedIcon
                    fontSize='large'
                    color='disabled'
                  />
                ) : (
                  <DeveloperBoardOutlinedIcon
                    fontSize='large'
                    color='primary'
                  />
                )}
              </ListItemIcon>
            </Tooltip>
            <ListItemText primary='Module creator' />
          </ListItem>
          <Divider />
          {/* **************************************************************** */}
          {systemConfig.mode === 'run' && (
            <ListItem
              button
              key='Dashboard'
              onClick={() => setItemState('Dashboard')}
            >
              <Tooltip title='Dashboard'>
                <ListItemIcon>
                  {!panelState.panel_3[0] ? (
                    <DashboardOutlinedIcon fontSize='large' color='disabled' />
                  ) : (
                    <DashboardOutlinedIcon fontSize='large' color='primary' />
                  )}
                </ListItemIcon>
              </Tooltip>
              <ListItemText primary='Dashboard' />
            </ListItem>
          )}
          <Divider />
          {/* **************************************************************** */}
        </List>
      </Drawer>
      <main className='MainWindow'>
        <div className={panelState.panel_0[0] ? 'showDiv' : 'hideByPos'}>
          Panel 1
        </div>
        <div className={panelState.panel_1[0] ? 'showDiv' : 'hideByPos'}>
          <PanelOne model={props.model} send_msg={props.send_msg} />
        </div>
        <div className={panelState.panel_2[0] ? 'showDiv' : 'hideByPos'}>
          Panel 3
        </div>
        <div className={panelState.panel_3[0] ? 'showDiv' : 'hideByPos'}>
          <DashBoardView
            model={props.model}
            send_msg={props.send_msg}
            displayStatus={panelState.panel_3[0] as boolean}
          />
        </div>
      </main>
    </div>
  );
};

const styles = (theme: any) => ({
  '@global': {
    // MUI typography elements use REMs, so you can scale the global
    // font size by setting the font-size on the <html> element.
    html: {
      fontSize: 12,
      [theme.breakpoints.up('sm')]: {
        fontSize: 12,
      },
      [theme.breakpoints.up('md')]: {
        fontSize: 13,
      },
      [theme.breakpoints.up('lg')]: {
        fontSize: 14,
      },
    },
  },
});

export default withStyles(styles)(SysExpUI);

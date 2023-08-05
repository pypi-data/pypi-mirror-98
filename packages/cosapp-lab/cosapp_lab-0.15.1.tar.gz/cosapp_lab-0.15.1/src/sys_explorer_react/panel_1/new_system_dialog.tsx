import React from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
import { useDispatch } from 'react-redux';
import { UserListType } from '../redux/types';
import * as ReduxAction from '../redux/actions';
import { createStyles, makeStyles, Theme } from '@material-ui/core/styles';
import FormControl from '@material-ui/core/FormControl';
import Autocomplete from '@material-ui/lab/Autocomplete';
import SystemCreatorDialog from './system_creator_dialog';
interface PropsInterface {
  open: boolean;
  handleClose: (path: any, name: string) => void;
  nodeData: { node: any; path: any };
}

const userList = [
  { uid: 0, name: 'LAC Etienne' },
  { uid: 1, name: 'DE SPIEGELEER Guy' },
  { uid: 2, name: 'COLLONVAL Frederic' },
  { uid: 3, name: 'THEOBALD Maurice' },
  { uid: 4, name: 'FEDERICI Thomas' },
  { uid: 5, name: 'LE Duc Trung' }
];

const systemList = [
  'Create new',
  'Demo system 1',
  'Demo system 2',
  'Demo system 3',
  'Demo system 4',
  'Demo system 5',
  'Demo system 6'
];

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    formControl: {
      padding: theme.spacing(1),
      minWidth: 300,
      width: '100%'
    },
    paperWidthSm: {
      maxWidth: 700
    }
  })
);

export function AddSystemDialog(props: PropsInterface) {
  const [sysName, setSysName] = React.useState<string>('');
  const [personName, setPersonName] = React.useState<UserListType[]>([]);
  const [sysClass, setSysClass] = React.useState<string>('Create new');
  const [switchForm, setSwitchForm] = React.useState<boolean>(true);
  const [portTableData, setPortTableData] = React.useState<any[]>([]);
  React.useEffect(() => {
    if (props.open) {
      setSysName('');
      setPersonName([]);
      setSysClass('Create new');
      setSwitchForm(true);
      setPortTableData([]);
    }
  }, [props.open]);
  const dispatch = useDispatch();

  const handleNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSysName(event.target.value);
  };

  const handleCreateNode = () => {
    if (sysClass !== 'Create new') {
      dispatch(
        ReduxAction.archAddNode(sysName, props.nodeData.path, {
          personName,
          sysClass,
          portList: []
        })
      );
      props.handleClose(null, '');
    } else {
      setSwitchForm(false);
    }
  };

  const handleCreateNewNode = () => {
    const portList = portTableData.map(value => ({
      portName: value.portName,
      portDirection: value.portDirection,
      portClass: value.portClass
    }));

    dispatch(
      ReduxAction.archAddNode(sysName, props.nodeData.path, {
        personName,
        sysClass,
        portList: portList
      })
    );
    props.handleClose(null, '');
  };

  const handleUserChange = (
    event: React.ChangeEvent<{}>,
    value: UserListType[]
  ) => {
    setPersonName(value);
  };

  const handleSysClassChange = (
    event: React.ChangeEvent<{}>,
    value: string
  ) => {
    setSysClass(value);
  };

  const classes = useStyles({});

  const addForm = (
    <DialogContent className={switchForm ? 'showDiv' : 'hideDiv'}>
      {/* <DialogContentText>Test</DialogContentText> */}
      <FormControl className={classes.formControl}>
        <TextField
          autoFocus
          margin="dense"
          label="System name"
          type="text"
          fullWidth
          value={sysName}
          onChange={handleNameChange}
        />
      </FormControl>
      <FormControl className={classes.formControl}>
        <Autocomplete
          onChange={handleUserChange}
          multiple
          options={userList}
          getOptionLabel={(option: UserListType) => option.name}
          renderInput={params => (
            <TextField
              {...params}
              variant="standard"
              label="Users (optional)"
              placeholder=""
              fullWidth
            />
          )}
        />
      </FormControl>
      <FormControl className={classes.formControl}>
        <Autocomplete
          value={sysClass}
          onChange={handleSysClassChange}
          options={systemList}
          getOptionLabel={(option: string) => option}
          defaultValue={systemList[0]}
          renderInput={params => (
            <TextField
              {...params}
              variant="standard"
              label="System catalog"
              placeholder=""
              fullWidth
            />
          )}
        />
      </FormControl>
    </DialogContent>
  );

  const createForm = (
    <DialogContent className={!switchForm ? 'showDiv' : 'hideDiv'}>
      <SystemCreatorDialog
        portTableData={portTableData}
        syncPortData={setPortTableData}
      />
    </DialogContent>
  );

  return (
    <div>
      <Dialog
        keepMounted={false}
        open={props.open as boolean}
        aria-labelledby="form-dialog-title"
        fullWidth={true}
        classes={{
          paperWidthSm: classes.paperWidthSm
        }}
        maxWidth="sm"
      >
        <DialogTitle id="form-dialog-title">
          {switchForm ? 'Add new system' : 'New system configuration'}
        </DialogTitle>
        {addForm}
        {createForm}
        {switchForm ? (
          <DialogActions>
            <Button onClick={() => props.handleClose(null, '')} color="primary">
              Cancel
            </Button>
            <Button onClick={handleCreateNode} color="primary">
              Add
            </Button>
          </DialogActions>
        ) : (
          <DialogActions>
            <Button onClick={() => props.handleClose(null, '')} color="primary">
              Cancel
            </Button>
            <Button onClick={() => setSwitchForm(true)} color="primary">
              Back
            </Button>
            <Button onClick={handleCreateNewNode} color="primary">
              Create
            </Button>
          </DialogActions>
        )}
      </Dialog>
    </div>
  );
}

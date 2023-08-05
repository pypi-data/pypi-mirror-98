import React, { Component } from 'react';
import { withStyles } from '@material-ui/core';
import { Styles } from '@material-ui/styles/withStyles';
import MaterialTable from 'material-table';

import { Theme } from '@material-ui/core/styles';
import { forwardRef } from 'react';
import AddBox from '@material-ui/icons/AddBox';
import ArrowDownward from '@material-ui/icons/ArrowDownward';
import Check from '@material-ui/icons/Check';
import ChevronLeft from '@material-ui/icons/ChevronLeft';
import ChevronRight from '@material-ui/icons/ChevronRight';
import Clear from '@material-ui/icons/Clear';
import DeleteOutline from '@material-ui/icons/DeleteOutline';
import Edit from '@material-ui/icons/Edit';
import FilterList from '@material-ui/icons/FilterList';
import FirstPage from '@material-ui/icons/FirstPage';
import LastPage from '@material-ui/icons/LastPage';
import Remove from '@material-ui/icons/Remove';
import SaveAlt from '@material-ui/icons/SaveAlt';
import Search from '@material-ui/icons/Search';
import ViewColumn from '@material-ui/icons/ViewColumn';

const tableIcons = {
  Add: forwardRef((props, ref: any) => <AddBox {...props} ref={ref} />),
  Check: forwardRef((props, ref: any) => <Check {...props} ref={ref} />),
  Clear: forwardRef((props, ref: any) => <Clear {...props} ref={ref} />),
  Delete: forwardRef((props, ref: any) => (
    <DeleteOutline {...props} ref={ref} />
  )),
  DetailPanel: forwardRef((props, ref: any) => (
    <ChevronRight {...props} ref={ref} />
  )),
  Edit: forwardRef((props, ref: any) => <Edit {...props} ref={ref} />),
  Export: forwardRef((props, ref: any) => <SaveAlt {...props} ref={ref} />),
  Filter: forwardRef((props, ref: any) => <FilterList {...props} ref={ref} />),
  FirstPage: forwardRef((props, ref: any) => (
    <FirstPage {...props} ref={ref} />
  )),
  LastPage: forwardRef((props, ref: any) => <LastPage {...props} ref={ref} />),
  NextPage: forwardRef((props, ref: any) => (
    <ChevronRight {...props} ref={ref} />
  )),
  PreviousPage: forwardRef((props, ref: any) => (
    <ChevronLeft {...props} ref={ref} />
  )),
  ResetSearch: forwardRef((props, ref: any) => <Clear {...props} ref={ref} />),
  Search: forwardRef((props, ref: any) => <Search {...props} ref={ref} />),
  SortArrow: forwardRef((props, ref: any) => (
    <ArrowDownward {...props} ref={ref} />
  )),
  ThirdStateCheck: forwardRef((props, ref: any) => (
    <Remove {...props} ref={ref} />
  )),
  ViewColumn: forwardRef((props, ref: any) => (
    <ViewColumn {...props} ref={ref} />
  )),
};

const styles: Styles<Theme, {}> = (theme: Theme) => ({});

interface AppState {
  columns: any;
  data: any;
}

interface AppProps {
  classes: any;
  portTableData: object[];
  syncPortData: (data: any[]) => void;
}
class SystemCreatorDialog extends Component<AppProps, AppState> {
  constructor(props: AppProps) {
    super(props);
    this.state = {
      columns: [
        {
          title: 'Port name',
          field: 'portName',
          cellStyle: {
            paddingLeft: 20,
          },
        },
        {
          title: 'Port direction',
          field: 'portDirection',
          lookup: { 0: 'Input', 1: 'Output' },
          initialEditValue: 0,
          cellStyle: {
            paddingLeft: 20,
          },
        },
        {
          title: 'Port class',
          field: 'portClass',
          lookup: { 0: 'Undefined', 1: 'Class 1' },
          initialEditValue: 0,
          cellStyle: {
            paddingLeft: 20,
          },
        },
      ],
      data: [],
      // data: this.props.portTableData
    };
  }

  render() {
    return (
      <MaterialTable
        //@ts-ignore
        icons={tableIcons}
        options={{
          headerStyle: {
            backgroundColor: '#3f51b5',
            color: '#FFF',
            paddingLeft: 20,
          },
        }}
        title=''
        columns={this.state.columns}
        data={this.state.data}
        editable={{
          onRowAdd: (newData) =>
            new Promise((resolve, reject) => {
              {
                const data = Array.from(this.state.data);
                data.push(newData);
                this.props.syncPortData(data);
                this.setState({ data }, () => resolve());
              }
              resolve();
            }),
          onRowUpdate: (newData, oldData) =>
            new Promise((resolve, reject) => {
              {
                const data = Array.from(this.state.data);
                const index = data.indexOf(oldData);
                data[index] = newData;
                this.props.syncPortData(data);
                this.setState({ data }, () => resolve());
              }
              resolve();
            }),
          onRowDelete: (oldData) =>
            new Promise((resolve, reject) => {
              {
                const data = Array.from(this.state.data);
                const index = data.indexOf(oldData);
                data.splice(index, 1);
                this.props.syncPortData(data);
                this.setState({ data }, () => resolve());
              }
              resolve();
            }),
        }}
      />
    );
  }
}

export default withStyles(styles)(SystemCreatorDialog);

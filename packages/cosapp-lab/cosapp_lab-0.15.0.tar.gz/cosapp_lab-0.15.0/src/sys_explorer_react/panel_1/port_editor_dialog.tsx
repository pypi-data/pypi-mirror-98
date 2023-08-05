import { withStyles } from '@material-ui/core';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogTitle from '@material-ui/core/DialogTitle';
import { Theme } from '@material-ui/core/styles';
import { Styles } from '@material-ui/styles/withStyles';
import React, { Component } from 'react';
import { connect } from 'react-redux';
import { StateInterface } from '../redux/types';

const styles: Styles<Theme, {}> = (theme: Theme) => ({});

interface AppProps {
  classes: any;
  open: boolean;
  switch: () => void;
}
interface AppState {}

const mapStateToProps = (state: StateInterface) => {
  return {};
};

const mapDispatchToProps = (dispatch: (f: any) => void) => {
  return {};
};

export class PortEditor extends Component<AppProps, AppState> {
  render() {
    const { classes } = this.props;
    return (
      <div>
        <Dialog
          keepMounted={false}
          open={this.props.open}
          aria-labelledby="form-dialog-title"
          fullWidth={true}
          classes={{
            paperWidthSm: classes.paperWidthSm
          }}
          maxWidth="md"
        >
          <DialogTitle id="form-dialog-title">{'Port editor'}</DialogTitle>
          {/* <DialogContent style={{ height: "50vh" }}>
            <TableContainer>
              <TableToolbar
                numSelected={Object.keys(selectedRowIds).length}
                deleteUserHandler={deleteUserHandler}
                addUserHandler={addUserHandler}
                preGlobalFilteredRows={preGlobalFilteredRows}
                setGlobalFilter={setGlobalFilter}
                globalFilter={globalFilter}
              />
              <MaUTable {...getTableProps()}>
                <TableHead>
                  {headerGroups.map((headerGroup) => (
                    <TableRow {...headerGroup.getHeaderGroupProps()}>
                      {headerGroup.headers.map((column) => (
                        <TableCell
                          {...(column.id === "selection"
                            ? column.getHeaderProps()
                            : column.getHeaderProps(
                                column.getSortByToggleProps()
                              ))}>
                          {column.render("Header")}
                          {column.id !== "selection" ? (
                            <TableSortLabel
                              active={column.isSorted}
                              // react-table has a unsorted state which is not treated here
                              direction={column.isSortedDesc ? "desc" : "asc"}
                            />
                          ) : null}
                        </TableCell>
                      ))}
                    </TableRow>
                  ))}
                </TableHead>
                <TableBody>
                  {page.map((row, i) => {
                    prepareRow(row);
                    return (
                      <TableRow {...row.getRowProps()}>
                        {row.cells.map((cell) => {
                          return (
                            <TableCell {...cell.getCellProps()}>
                              {cell.render("Cell")}
                            </TableCell>
                          );
                        })}
                      </TableRow>
                    );
                  })}
                </TableBody>

                <TableFooter>
                  <TableRow>
                    <TablePagination
                      rowsPerPageOptions={[
                        5,
                        10,
                        25,
                        { label: "All", value: data.length },
                      ]}
                      colSpan={3}
                      count={data.length}
                      rowsPerPage={pageSize}
                      page={pageIndex}
                      SelectProps={{
                        inputProps: { "aria-label": "rows per page" },
                        native: true,
                      }}
                      onChangePage={handleChangePage}
                      onChangeRowsPerPage={handleChangeRowsPerPage}
                      ActionsComponent={TablePaginationActions}
                    />
                  </TableRow>
                </TableFooter>
              </MaUTable>
            </TableContainer>
          </DialogContent> */}
          <DialogActions>
            <Button onClick={this.props.switch} color="primary">
              Close
            </Button>
            <Button color="primary">Create</Button>
          </DialogActions>
        </Dialog>
      </div>
    );
  }
}

export default withStyles(styles)(
  connect(mapStateToProps, mapDispatchToProps)(PortEditor)
);

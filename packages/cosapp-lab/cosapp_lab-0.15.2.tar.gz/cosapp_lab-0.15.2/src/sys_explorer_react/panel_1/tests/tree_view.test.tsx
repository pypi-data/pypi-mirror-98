import { Provider } from 'react-redux';
import { panel1MockState } from  '../../../utils/tests/store_mock' ;
import { MockModel } from '../../../utils/tests/utils';
import React from 'react';
import {
  configure,
  shallow,
  ShallowWrapper,
  ReactWrapper,
  mount,
} from 'enzyme';
import Adapter from '@wojtekmaj/enzyme-adapter-react-17';
import TreePanel, {
  ViewButton,
  TreePanel as PureTreePanel,
} from '../tree_view';
import thunk from 'redux-thunk';
import configureMockStore from 'redux-mock-store';
import IconButton from '@material-ui/core/IconButton';

configure({ adapter: new Adapter() });

const mockStore = configureMockStore([thunk]);

describe('Test <TreePanel/>', () => {
  let wrapper: ShallowWrapper;
  beforeEach(() => {
    const store = mockStore({
      ...panel1MockState,
    });
    wrapper = shallow(
      <Provider store={store}>
        <TreePanel model={new MockModel() as any} send_msg={jest.fn()} />
      </Provider>
    );
  });

  afterEach(() => {
    wrapper.unmount();
  });

  it('Should render correctly component', () => {
    const component = wrapper.find(TreePanel);
    expect(component).toHaveLength(1);
  });
});

describe('Test <PureTreePanel/>', () => {
  let wrapper: ShallowWrapper<{}, {}, PureTreePanel>;
  let treeDataChanged: jest.Mock;
  let removeTreeNode: jest.Mock;
  let lockGraph: jest.Mock;
  let updateFilter: jest.Mock;
  let model: any;
  let send_msg: any;
  beforeEach(() => {
    treeDataChanged = jest.fn((treeData: any) => {});
    removeTreeNode = jest.fn((node: any, path: any) => {});
    lockGraph = jest.fn((status: boolean) => {});
    updateFilter = jest.fn((data: Array<string>) => {});
    send_msg = jest.fn(() => {});
    wrapper = shallow(
      <PureTreePanel
        classes={''}
        treeData={panel1MockState.systemArch.systemTree.nodeData}
        treeDataChanged={treeDataChanged}
        removeTreeNode={removeTreeNode}
        lockGraph={lockGraph}
        updateFilter={updateFilter}
        systemConfig = {{}}
        graphPosition = {{}}
        selectedNode = ""
        saveGraphPosition = {jest.fn()}
        model={new MockModel() as any}
        send_msg={jest.fn()}
        updateConnectionGraph = {jest.fn()}
        updateSelectedNode = {jest.fn()}
      />
    );
  });

  afterEach(() => {
    wrapper.unmount();
  });

  it('Should render correctly component', () => {
    const component = wrapper.find('div');
    expect(component).toHaveLength(4);
  });

  it('Should close dialog with closeNewSystemDialog()', () => {
    wrapper.instance().closeNewSystemDialog();
    expect(lockGraph).toBeCalledTimes(1);
    expect(wrapper.state()['newSystemDialog']).toEqual(false);
  });

  it('Should start with default state ', () => {
    const defaultState = {
      activatedTreeNode: {},
      currentNodeData: { node: null, path: null },
      newSystemDialog: false,
      portEditorState: false,
      treeNodeResetSignal: 0,
      expandNotification: false,
      helpDialog: false,
      serverLog: 'Starting server, please wait...',
      serverToken: ''
    };
    expect(wrapper.state()).toEqual(defaultState);
  });

  it('Should update activatedTreeNode with updateState() ', () => {
    const defaultState = { root: true };
    wrapper.instance().updateState({ id: 'root' }, true);
    expect(wrapper.state()['activatedTreeNode']).toEqual(defaultState);
  });

  it('Should clear activatedTreeNode with clearFilterView() ', () => {
    wrapper.instance().clearFilterView();
    expect(updateFilter).toBeCalledTimes(1);
    expect(wrapper.state()['treeNodeResetSignal']).toEqual(1);
  });
});

describe('Test <ViewButton/>', () => {
  let wrapper: ReactWrapper;
  let btnHandle: jest.Mock;
  let btn: ReactWrapper;
  beforeEach(() => {
    btnHandle = jest.fn((node: any, value: boolean) => {});
    wrapper = mount(
      <ViewButton
        node={'root'}
        path={0}
        updateState={btnHandle}
        resetSignal={0}
      />
    );
    btn = wrapper.find(IconButton);
  });

  afterEach(() => {
    wrapper.unmount();
  });

  it('Should match the snapshot', () => {
    const component = wrapper;
    expect(component.html()).toMatchSnapshot();
  });

  it('Should switch state on click', () => {
    expect(wrapper.state('checked')).toEqual(false);
    btn.simulate('click');
    expect(wrapper.state('checked')).toEqual(true);
  });

  it('Should call `props.updateState` in click', () => {
    expect(btnHandle).toBeCalledTimes(1);
    btn.simulate('click');
    expect(btnHandle).toBeCalledTimes(2);
  });
});

import { Provider } from 'react-redux';
import { initialState } from '../../redux/reducers';
import React from 'react';
import { configure,  mount, ReactWrapper } from 'enzyme';
import Adapter from '@wojtekmaj/enzyme-adapter-react-17';
import ControlPanel from '../control_panel';
import thunk from 'redux-thunk';
import configureMockStore from 'redux-mock-store';
import Fab from '@material-ui/core/Fab';

configure({ adapter: new Adapter() });

const mockStore = configureMockStore([thunk]);

describe('Test <ControlPanel/>', () => {
  let wrapper: ReactWrapper;
  let btnHandle;

  beforeEach(() => {
    const store = mockStore({
      ...initialState
    });
    btnHandle = jest.fn(() => {});
    wrapper = mount(
      <Provider store={store}>
        <ControlPanel runBtnHandle={btnHandle} logMsg={''} />
      </Provider>
    );
  });

  afterEach(() => {
    wrapper.unmount();
  });

  it('Should render correctly component', () => {
    const component = wrapper.find(ControlPanel);
    expect(component).toHaveLength(1);
  });

  it('Should open add controller dialog when add button clicked', () => {
    const component = wrapper
      .find(ControlPanel)
      .childAt(0)
      .childAt(0);
    const addButton = component.find(Fab).at(0);
    expect(component.state('addVariableDialog')).toEqual(false);
    addButton.simulate('click');
    expect(component.state('addVariableDialog')).toEqual(true);
  });

  it('Should call run function when run button clicked', () => {
    const component = wrapper
      .find(ControlPanel)
      .childAt(0)
      .childAt(0);
    const runButton = component.find(Fab).at(1);
    runButton.simulate('click');
    expect(btnHandle).toBeCalled();
  });
});

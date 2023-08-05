import { Provider } from 'react-redux';
import { initialState } from '../../redux/reducers';
import React from 'react';
import { configure, mount, ReactWrapper } from 'enzyme';
import Adapter from '@wojtekmaj/enzyme-adapter-react-17';
import { AddSystemDialog } from '../new_system_dialog';
import thunk from 'redux-thunk';
import configureMockStore from 'redux-mock-store';
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import Button from '@material-ui/core/Button';
import DialogContent from '@material-ui/core/DialogContent';

configure({ adapter: new Adapter() });

const mockStore = configureMockStore([thunk]);

describe('Test <AddSystemDialog/>', () => {
  let wrapper: ReactWrapper;
  beforeEach(() => {
    const store = mockStore({
      ...initialState
    });
    wrapper = mount(
      <Provider store={store}>
        <AddSystemDialog
          open={true}
          handleClose={(path: any, name: string) => {}}
          nodeData={{ node: null, path: null }}
        />
      </Provider>
    );
    console.log('wrapper', wrapper)
  });

  afterEach(() => {
    wrapper.unmount();
  });

  it('Should render correctly component', () => {
    const component = wrapper.find(AddSystemDialog).at(0);
    expect(component).toHaveLength(1);
  });

  it('Should render the component with default value in inputs', () => {
    const component = wrapper.find(AddSystemDialog).at(0);
    const inputLength = 4;
    const defaultInput = [
      'System name',
      'Users (optional)',
      'System catalog',
      ''
    ];
    const textField = component.find(TextField);
    expect(textField).toHaveLength(inputLength);
    for (let index = 0; index < inputLength; index++) {
      expect(textField.at(index).text()).toEqual(defaultInput[index]);
    }
  });

  it('System catalog with default value', () => {
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

    const component = wrapper.find(AddSystemDialog).at(0);
    const userSelector = component.find(Autocomplete).at(0);
    const classSelector = component.find(Autocomplete).at(1);
    expect(userSelector.prop('options')).toEqual(userList);
    expect(classSelector.prop('options')).toEqual(systemList);
  });

  it('Click add button with new class', () => {
    const component = wrapper.find(AddSystemDialog).at(0);
    const addBtn = component.find(Button).at(1);
    expect(addBtn.text()).toEqual('Add');
    const dialogContent = component.find(DialogContent);
    expect(dialogContent).toHaveLength(2);
    expect(dialogContent.at(0).hasClass('showDiv')).toEqual(true);
    expect(dialogContent.at(1).hasClass('hideDiv')).toEqual(true);
    addBtn.simulate('click');
    expect(addBtn.text()).toEqual('Back');
  });
});

import { Provider } from 'react-redux';
import { initialState } from '../../redux/reducers';
import React from 'react';
import { configure,  mount } from 'enzyme';
import Adapter from '@wojtekmaj/enzyme-adapter-react-17';
import ParameterController from '../param_controller';
import thunk from 'redux-thunk';
import configureMockStore from 'redux-mock-store';
configure({ adapter: new Adapter() });

const mockStore = configureMockStore([thunk]);

describe('Test <ParameterController/>', () => {
  let wrapper: any;
  beforeEach(() => {
    const store = mockStore({
      ...initialState
    });
    wrapper = mount(
      <Provider store={store}>
        <ParameterController
          variableName='selectedVar'
          key='selectedVar'
          value={0}
        />
      </Provider>
    );
  });

  afterEach(() => {
    wrapper.unmount();
  });

  it('Should render correctly component', () => {
    const component = wrapper.find(ParameterController);
    expect(component).toHaveLength(1);
  });

  it('Should match snapshot', () => {
    const component = wrapper.find(ParameterController);
    expect(component.html()).toMatchSnapshot();
  });
});

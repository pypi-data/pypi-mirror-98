import { Provider } from 'react-redux';
import { initialState } from '../../redux/reducers';
import React from 'react';
import { configure, mount, ReactWrapper } from 'enzyme';
import Adapter from '@wojtekmaj/enzyme-adapter-react-17';
import SystemCreatorDialog from '../system_creator_dialog';
import thunk from 'redux-thunk';
import configureMockStore from 'redux-mock-store';

configure({ adapter: new Adapter() });

const mockStore = configureMockStore([thunk]);

describe('Test <SystemCreatorDialog/>', () => {
  let wrapper: ReactWrapper;
  beforeEach(() => {
    const store = mockStore({
      ...initialState
    });
    wrapper = mount(
      <Provider store={store}>
        <SystemCreatorDialog
          portTableData={[]}
          syncPortData={(data: any[]) => {}}
        />
      </Provider>
    );
  });

  afterEach(() => {
    wrapper.unmount();
  });

  it('Should render correctly component', () => {
    const component = wrapper.find(SystemCreatorDialog);
    expect(component).toHaveLength(1);
  });
  it('Should render correctly default table', () => {
    const component = wrapper.find(SystemCreatorDialog);
    expect(
      component.find('tr.MuiTableRow-root.MuiTableRow-head').html()
    ).toMatchSnapshot();
  });
});

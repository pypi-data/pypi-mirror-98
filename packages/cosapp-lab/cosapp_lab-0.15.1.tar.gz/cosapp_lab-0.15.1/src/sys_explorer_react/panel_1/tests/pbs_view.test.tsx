import { Provider } from 'react-redux';
import { panel1MockState } from '../../../utils/tests/store_mock';
import React from 'react';
import { configure, shallow, ShallowWrapper, ReactWrapper, mount } from 'enzyme';
import Adapter from '@wojtekmaj/enzyme-adapter-react-17';
import  {PBSPanel2 } from '../pbs_view_2';
configure({ adapter: new Adapter() });

describe('Test <PBSPanel2/>', () => {
  let wrapper: ShallowWrapper<{},{},PBSPanel2 >;
  let saveGraphPosition: jest.Mock;
  beforeEach(() => {
    saveGraphPosition = jest.fn((data :  any) => {});

    wrapper = shallow(
        <PBSPanel2 
            classes = {''} 
            pbsData = {panel1MockState.systemArch.systemTree} 
            signal = {0}
            positionData = {panel1MockState.systemArch.systemPBS}
            systemPBSUpdated = {0}
            saveGraphPosition = {saveGraphPosition}
          />
    );
  });

  afterEach(() => {
    wrapper.unmount();
  });

  it('Should render correctly component', () => {
    const component = wrapper.find('div');    
    expect(component).toHaveLength(3);     
  });

});


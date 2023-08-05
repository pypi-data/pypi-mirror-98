import { Provider } from 'react-redux';
import { initialState } from '../../redux/reducers';
import React from 'react';
import { configure, shallow, ShallowWrapper } from 'enzyme';
import Adapter from '@wojtekmaj/enzyme-adapter-react-17';
import GraphPanel, { GraphPanel as OriginalGraphPanel } from '../graph_view';
import thunk from 'redux-thunk';
import configureMockStore from 'redux-mock-store';
import { createShallow } from '@material-ui/core/test-utils';

configure({ adapter: new Adapter() });

const mockStore = configureMockStore([thunk]);

describe('Test <GraphPanel/>', () => {
  let shallow_: typeof shallow;
  let wrapper: ShallowWrapper;

  beforeAll(() => {
    shallow_ = createShallow();
  });

  beforeEach(() => {
    const store = mockStore({
      ...initialState
    });
    wrapper = shallow_(
      <Provider store={store}>
        <GraphPanel signal = {1}/>
      </Provider>
    );
  });

  afterEach(() => {
    wrapper.unmount();
  });

  it('Should render correctly component', () => {
    const component = wrapper.find(GraphPanel);
    expect(component).toHaveLength(1);
  });

  it('Test createNode()', () => {
    const node = OriginalGraphPanel.createNode('test', ['inPort'], ['outPort']);
    expect(node.getOptions()['color']).toEqual('rgb(0,192,255)');
    expect(node.getOptions()['name']).toEqual('test');
    expect(node.getOptions()['type']).toEqual('default');
    expect(node.getInPorts()).toHaveLength(1);
    expect(node.getInPorts()[0].getName()).toEqual('inPort');
    expect(node.getOutPorts()).toHaveLength(1);
    expect(node.getOutPorts()[0].getName()).toEqual('outPort');
  });

  it.each`
    sysName         | link                                   | result
    ${'test'}       | ${['inwards', 'test2.outwards']}       | ${['test.test2', 'test', 'outwards', 'inwards']}
    ${'test'}       | ${['test1.inwards', 'test2.outwards']} | ${['test.test2', 'test.test1', 'outwards', 'inwards']}
    ${'test.test1'} | ${['test2.inwards', 'outwards']}       | ${['test.test1', 'test.test1.test2', 'outwards', 'inwards']}
    ${'test.test1'} | ${['test2.inwards', 'test3.outwards']} | ${['test.test1.test3', 'test.test1.test2', 'outwards', 'inwards']}
  `(
    'createLink() should return $result with "$sysName" and $link as input  ',
    ({ sysName, link, result }) => {
      const {
        startSys,
        endSys,
        startPort,
        endPort
      } = OriginalGraphPanel.createLink(sysName, link);
      expect(startSys).toEqual(result[0]);
      expect(endSys).toEqual(result[1]);
      expect(startPort).toEqual(result[2]);
      expect(endPort).toEqual(result[3]);
    }
  );
});

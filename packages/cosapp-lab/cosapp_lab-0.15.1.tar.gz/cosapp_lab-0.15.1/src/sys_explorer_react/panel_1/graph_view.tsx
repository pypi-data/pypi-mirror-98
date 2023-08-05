import { withStyles } from '@material-ui/core';
import Button from '@material-ui/core/Button';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import { Theme } from '@material-ui/core/styles';
import SettingsIcon from '@material-ui/icons/Settings';
import { Styles } from '@material-ui/styles/withStyles';
import { CanvasWidget } from '@projectstorm/react-canvas-core';
import createEngine, {
  DagreEngine,
  DefaultDiagramState,
  DiagramModel,
  PathFindingLinkFactory
} from '@projectstorm/react-diagrams';
import { DiagramEngine } from '@projectstorm/react-diagrams-core';
import React, { Component } from 'react';
import { connect } from 'react-redux';
import * as ReduxAction from '../redux/actions';
import { StateInterface, SystemGraphInterface } from '../redux/types';
import { BaseCanvasWidget } from './canvas_widget';
import {
  AdvancedLinkFactory,
  AdvancedLinkModel,
  CustomNodeFactory,
  CustomNodeModel,
  CustomPortModel
} from './custom_link';

const styles: Styles<Theme, {}> = (theme: Theme) => ({});

const getGraphData = (state: StateInterface) => {
  return {
    systemData: state.systemArch.systemGraph,
    lockStatus: state.systemArch.lockStatus,
    saveSignal: state.saveSignal,
    graphJsonData: state.systemArch.systemGraph.graphJsonData,
    pbsNodePosition: state.systemArch.systemPBS,
    treeSelectedNode: state.systemArch.systemTree.nodePath
  };
};

const mapStateToProps = (state: StateInterface) => {
  return getGraphData(state);
};

const mapDispatchToProps = (dispatch: (f: any) => void) => {
  return {
    saveGraphJson: (data: { [key: string]: any }) =>
      dispatch(ReduxAction.archSaveGraphJson(data))
  };
};

interface AppState {
  engine: DiagramEngine;
  model: DiagramModel;
  nodeData: { [key: string]: CustomNodeModel };
  filterMenuToggle: boolean;
  filterMode: number;
}

interface AppProps {
  classes: any;
  systemData: SystemGraphInterface; // data to draw the graph;
  lockStatus: boolean; // flag for editing the graph;
  saveSignal: number; // signal to save the graph to json file;
  saveGraphJson: (data: { [key: string]: any }) => void; // action to save graph json into store;
  graphJsonData: { [key: string]: any };
  pbsNodePosition: {
    [key: string]: { visible: boolean; position: Array<number> };
  }; // Position of node from PBS view;
  signal: number; // Tab ID, used to rerender the graph when the tab is switched;
  treeSelectedNode: Array<string>; // List of node selected in tree view
}

const FILTER_MODE = Object.freeze({ 0: 'selected nodes', 1: 'all nodes' });

export class GraphPanel extends Component<AppProps, AppState> {
  graphEngine: DagreEngine;
  engine: DiagramEngine;
  model: DiagramModel;
  private filterBtnRef: React.RefObject<HTMLButtonElement>;

  constructor(props: AppProps) {
    super(props);

    this.filterBtnRef = React.createRef<HTMLButtonElement>();
    this.engine = createEngine();
    this.graphEngine = new DagreEngine({
      graph: {
        rankdir: 'TB',
        ranker: 'longest-path',
        align: 'DL',
        marginx: 100,
        marginy: 100
      },
      includeLinks: false
    });
    this.engine.getLinkFactories().registerFactory(new AdvancedLinkFactory());
    this.engine.getNodeFactories().registerFactory(new CustomNodeFactory());
    this.model = new DiagramModel();
    const engineState = this.engine.getStateMachine().getCurrentState();
    if (engineState instanceof DefaultDiagramState) {
      engineState.dragNewLink.config.allowLooseLinks = false;
    }
    this.engine.setModel(this.model);
    this.state = {
      engine: this.engine,
      model: this.model,
      nodeData: {},
      filterMenuToggle: false,
      filterMode: 0
    };
  }

  /**
   *  This function extract the data from a `AdvancedLinkModel`
   *  and return the target and source port of this link with
   *  correct system name.
   *
   * @static
   * @param {AdvancedLinkModel} linkElement
   * @returns
   * @memberof GraphPanel
   */
  static connectionDataGenerator(linkElement: AdvancedLinkModel) {
    const sourcePort = linkElement.getSourcePort();
    const sourcePortName: string = sourcePort.getName();
    const sourceSystem: string = sourcePort.getParent().getOptions()['name'];
    const targetPort = linkElement.getTargetPort();
    const targetPortName: string = targetPort.getName();
    const targetSystem: string = targetPort.getParent().getOptions()['name'];
    let connection: string[];
    let sysKey: string;
    if (!targetSystem.includes('.')) {
      sysKey = targetSystem;
      connection = [
        targetPortName,
        sourceSystem.replace(sysKey + '.', '') + '.' + sourcePortName
      ];
    } else {
      if (!sourceSystem.includes('.')) {
        sysKey = sourceSystem;
        connection = [
          targetSystem.replace(sysKey + '.', '') + '.' + targetPortName,
          sourcePortName
        ];
      } else {
        const sourceSysArray = sourceSystem.split('.');
        const targetSysArray = targetSystem.split('.');
        sysKey = sourceSysArray[0];

        for (
          let index = 1;
          index < Math.min(sourceSysArray.length, targetSysArray.length);
          index++
        ) {
          if (sourceSysArray[index] === targetSysArray[index]) {
            sysKey = sysKey.concat('.' + sourceSysArray[index]);
          } else {
            break;
          }
        }
        const targetConnection =
          targetSystem.replace(sysKey, '') + '.' + targetPortName;
        const sourceConnection =
          sourceSystem.replace(sysKey, '') + '.' + sourcePortName;
        connection = [
          targetConnection.replace(/^./, ''),
          sourceConnection.replace(/^./, '')
        ];
      }
    }
    return { sysKey, connection };
  }

  /**
   * This function contains the logic to save the graph each
   * time the `saveSignal` is updated and to update the node positions
   * each time the tab is activated
   * @param {AppProps} prevProps
   * @param {AppState} prevState
   * @memberof GraphPanel
   */
  componentDidUpdate(prevProps: AppProps, prevState: AppState) {
    if (prevProps.saveSignal !== this.props.saveSignal) {
      const connectionData = {};
      const positionData = {};
      this.model.getLinks().forEach((linkElement: AdvancedLinkModel) => {
        const { sysKey, connection } = GraphPanel.connectionDataGenerator(
          linkElement
        );
        if (Object.keys(connectionData).includes(sysKey)) {
          connectionData[sysKey].push(connection);
        } else {
          connectionData[sysKey] = [connection];
        }
      });
      this.model.getNodes().forEach(nodeElement => {
        const nodeName = nodeElement.getOptions()['name'];
        positionData[nodeName] = [nodeElement.getX(), nodeElement.getY()];
      });
      this.props.saveGraphJson({
        position: positionData,
        connection: connectionData
      });
    }

    if (prevProps.signal != this.props.signal && this.props.signal == 1) {
      setTimeout(() => {
        this.syncPosition();
      }, 200);
    } else if (
      this.props.signal == 1 &&
      prevProps.pbsNodePosition != this.props.pbsNodePosition
    ) {
      setTimeout(() => {
        this.syncPosition();
      }, 200);
    }
  }

  /**
   * This function create the link data from system name
   * and connection.
   *
   * @static
   * @param {string} systemName
   * @param {string[]} connection
   * @returns
   * @memberof GraphPanel
   */
  static createLink(systemName: string, connection: string[]) {
    const start = connection[1];
    const end = connection[0];
    let startSys, endSys, startPort, endPort;
    if (start.includes('.')) {
      const sysArray = start.split('.');
      startPort = sysArray[sysArray.length - 1];
      startSys =
        systemName + '.' + sysArray.slice(0, sysArray.length - 1).join('.');
    } else {
      startSys = systemName;
      startPort = start;
    }
    if (end.includes('.')) {
      const sysArray = end.split('.');
      endPort = sysArray[sysArray.length - 1];
      endSys =
        systemName + '.' + sysArray.slice(0, sysArray.length - 1).join('.');
    } else {
      endSys = systemName;
      endPort = end;
    }
    return { startSys, endSys, startPort, endPort };
  }

  /**
   *
   *
   * @private
   * @memberof GraphPanel
   */
  private createNodeFromData = (
    propsData: SystemGraphInterface,
    systemList: string[] = []
  ): { [key: string]: CustomNodeModel } => {
    const newNodeData: { [key: string]: CustomNodeModel } = {};
    for (let index = 0; index < propsData.systemList.length; index++) {
      const sysName = propsData.systemList[index];
      if (systemList.length > 0 && !systemList.includes(sysName)) {
        continue;
      }
      const inPortList = propsData.systemGraphData[sysName].inPort;
      const outPortList = propsData.systemGraphData[sysName].outPort;

      const node: CustomNodeModel = GraphPanel.createNode(
        sysName,
        inPortList,
        outPortList
      );

      if (!(propsData.systemGraphData[sysName].position == null)) {
        const nodeX: number = propsData.systemGraphData[sysName].position[0];
        const nodeY: number = propsData.systemGraphData[sysName].position[1];
        node.setPosition(nodeX, nodeY);
      }
      newNodeData[sysName] = node;
    }
    return newNodeData;
  };

  private creatConnectionFromData = (
    propsData: SystemGraphInterface,
    newNodeData: { [key: string]: CustomNodeModel },
    pathfinding: any,
    relatedNode: string[] = []
  ) => {
    const linkList = [];
    propsData.systemList.forEach(systemName => {
      if (relatedNode.length > 0 && !relatedNode.includes(systemName)) {
        return;
      }
      const connectionList: Array<Array<string>> =
        propsData.systemGraphData[systemName].connections;
      connectionList.forEach(connection => {
        const { startSys, endSys, startPort, endPort } = GraphPanel.createLink(
          systemName,
          connection
        );
        const nodeStart = newNodeData[startSys];
        const nodeEnd = newNodeData[endSys];

        if (
          nodeStart.getPorts().hasOwnProperty(startPort) &&
          nodeEnd.getPorts().hasOwnProperty(endPort)
        ) {
          const portSource = nodeStart.getPorts()[startPort] as CustomPortModel;
          const portSink = nodeEnd.getPorts()[endPort] as CustomPortModel;

          const link = portSource.link(portSink, pathfinding);
          linkList.push(link);
        }
      });
    });

    return linkList;
  };

  /**
   * The connection graph is created in componentDidMount method
   *
   * @memberof GraphPanel
   */
  componentDidMount() {
    this.model.setLocked(this.props.lockStatus);

    const newNodeData = this.createNodeFromData(this.props.systemData);
    Object.values(newNodeData).forEach(node => {
      this.model.addNode(node);
    });

    const pathfinding = this.engine
      .getLinkFactories()
      .getFactory<PathFindingLinkFactory>(PathFindingLinkFactory.NAME);
    const linkList = this.creatConnectionFromData(
      this.props.systemData,
      newNodeData,
      pathfinding
    );

    linkList.forEach(element => {
      this.model.addLink(element);
    });

    this.setState(
      () => ({
        engine: this.engine,
        model: this.model,
        nodeData: newNodeData
      }),
      () => {
        setTimeout(this.syncPosition, 500);
      }
    );
  }

  /**
   * This function compute the zoom factor from
   * the  bounding box of the graph and the `margin`
   *
   * @private
   * @memberof GraphPanel
   */
  private autoZoomGraph = (margin?: number) => {
    const engine = this.state.engine;
    const model = this.state.model;
    const allNodes = model
      .getNodes()
      .filter((node: CustomNodeModel) => node.isVisible())
      .map(node => node) as Array<CustomNodeModel>;
    const nodesRect = engine.getBoundingNodesRect(allNodes, margin);
    if (nodesRect) {
      // there is something we should zoom on

      const canvasRect = engine.getCanvas().getBoundingClientRect();
      const canvasTopLeftPoint = {
        x: canvasRect.left,
        y: canvasRect.top
      };
      const nodeLayerTopLeftPoint = {
        x: canvasTopLeftPoint.x + model.getOffsetX(),
        y: canvasTopLeftPoint.y + model.getOffsetY()
      };

      const xFactor = engine.getCanvas().clientWidth / nodesRect.getWidth();
      const yFactor = engine.getCanvas().clientHeight / nodesRect.getHeight();
      const zoomFactor = xFactor < yFactor ? xFactor : yFactor;

      this.model.setZoomLevel(zoomFactor * 100);

      const nodesRectTopLeftPoint = {
        x: nodeLayerTopLeftPoint.x + nodesRect.getTopLeft().x * zoomFactor,
        y: nodeLayerTopLeftPoint.y + nodesRect.getTopLeft().y * zoomFactor
      };
      const width = nodesRect.getWidth() * zoomFactor;
      const height = nodesRect.getHeight() * zoomFactor;
      const hOffset = (canvasRect.width - width) / 2;
      const vOffset = (canvasRect.height - height) / 2;
      this.model.setOffset(
        this.model.getOffsetX() +
          canvasTopLeftPoint.x -
          nodesRectTopLeftPoint.x +
          hOffset,
        this.model.getOffsetY() +
          canvasTopLeftPoint.y -
          nodesRectTopLeftPoint.y +
          vOffset
      );

      engine.repaintCanvas();
    }
  };

  /**
   * Update node position by using Dagre
   *
   * @memberof GraphPanel
   */
  autoDistribute = () => {
    this.graphEngine.redistribute(this.state.model);
    this.reroute();
    this.state.engine.repaintCanvas();
    this.autoZoomGraph(50);
  };

  reroute = () => {
    this.state.engine
      .getLinkFactories()
      .getFactory<PathFindingLinkFactory>(PathFindingLinkFactory.NAME)
      .calculateRoutingMatrix();
  };

  /**
   * Switch the read-only flag of graph
   *
   * @memberof GraphPanel
   */
  lockModel = (state: boolean) => {
    this.state.model.setLocked(state);
  };

  /**
   * Create a `CustomNodeModel` from system name and
   * list of in/out port
   *
   * @static
   * @param {string} sysName
   * @param {string[]} inPortList
   * @param {string[]} outPortList
   * @returns
   * @memberof GraphPanel
   */
  static createNode(
    sysName: string,
    inPortList: string[],
    outPortList: string[]
  ) {
    const node = new CustomNodeModel(sysName, 'rgb(0,192,255)');

    inPortList.forEach(portName => {
      const inp = new CustomPortModel(true, portName, portName);

      node.addPort(inp);
    });
    outPortList.forEach(portName => {
      const outp = new CustomPortModel(false, portName, portName);

      node.addPort(outp);
    });
    return node;
  }

  /**
   * Update the graph if the input data is changed
   *
   * @param {AppProps} newProps
   * @memberof GraphPanel
   */
  UNSAFE_componentWillReceiveProps(newProps: AppProps) {
    if (newProps.lockStatus !== this.props.lockStatus) {
      this.lockModel(newProps.lockStatus);
    }

    const currentModel = this.state.model;
    let newNodeData: { [key: string]: CustomNodeModel } = {};
    if (
      newProps.systemData.systemList.length >
      this.props.systemData.systemList.length
    ) {
      newProps.systemData.systemList.forEach(sysName => {
        const inPortList = newProps.systemData.systemGraphData[sysName].inPort;
        const outPortList =
          newProps.systemData.systemGraphData[sysName].outPort;
        if (!this.props.systemData.systemList.includes(sysName)) {
          const node = GraphPanel.createNode(sysName, inPortList, outPortList);
          currentModel.addNode(node);
          newNodeData = { ...this.state.nodeData, [sysName]: node };
        }
      });
      this.setState({
        ...this.state,
        model: currentModel,
        nodeData: newNodeData
      });
    } else if (
      newProps.systemData.systemList.length <
      this.props.systemData.systemList.length
    ) {
      this.props.systemData.systemList.forEach(sysName => {
        if (!newProps.systemData.systemList.includes(sysName)) {
          const linkList = Object.values(currentModel.getLinks());
          linkList.forEach(link => {
            const srcPort = link.getSourcePort();
            const targetPort = link.getTargetPort();
            if (
              //@ts-ignore
              srcPort.getParent().getOptions().name === sysName ||
              //@ts-ignore
              targetPort.getParent().getOptions().name === sysName
            ) {
              currentModel.removeLink(link);
            }
          });

          currentModel.removeNode(this.state.nodeData[sysName]);
          const { [sysName]: nodeData, ...temp } = this.state.nodeData;
          newNodeData = temp;
        }
      });
      this.setState({
        ...this.state,
        model: currentModel,
        nodeData: newNodeData
      });
    } else {
      if (newProps.systemData.systemList != this.props.systemData.systemList) {
        const updateData = newProps.systemData.updateData;

        const removedSys = Object.keys(updateData);
        const addedSys = Object.values(updateData);
        const currentNodeData = { ...this.state.nodeData };
        const updatedNodeData = this.createNodeFromData(
          newProps.systemData,
          addedSys
        );

        for (const [key, value] of Object.entries(updateData)) {
          if (Object.keys(this.state.nodeData).includes(key)) {
            this.model.removeNode(currentNodeData[key]);
            this.model.addNode(updatedNodeData[value]);
            delete currentNodeData[key];
            currentNodeData[value] = updatedNodeData[value];
          }
        }

        const linkList = Object.values(this.model.getLinks());

        linkList.forEach(link => {
          const srcPort = link.getSourcePort();
          const targetPort = link.getTargetPort();
          if (
            //@ts-ignore
            removedSys.includes(srcPort.getParent().getOptions().name) ||
            //@ts-ignore
            removedSys.includes(targetPort.getParent().getOptions().name)
          ) {
            this.model.removeLink(link);
          }
        });

        const pathfinding = this.engine
          .getLinkFactories()
          .getFactory<PathFindingLinkFactory>(PathFindingLinkFactory.NAME);

        const newLinkList = this.creatConnectionFromData(
          newProps.systemData,
          currentNodeData,
          pathfinding,
          addedSys
        );

        newLinkList.forEach(link => {
          this.model.addLink(link);
        });
        this.setState(oldState => ({
          ...oldState,
          model: this.model,
          nodeData: currentNodeData
        }));
      }
    }
  }

  /**
   * Update node position from PBS view
   *
   * @private
   * @memberof GraphPanel
   */
  private syncPosition = () => {
    const currentModel = this.state.model;
    const disabledNode = [];
    const nodes = currentModel.getNodes() as Array<CustomNodeModel>;
    const radial = this.props.pbsNodePosition['__$graph_style$__'].visible;

    let scaleFactor = 3;
    if (radial) {
      scaleFactor = 1;
    }
    const nodeMode = this.state.filterMode;
    const selectedNode = this.props.treeSelectedNode;

    nodes.forEach(node => {
      const nodeName = node.getOptions()['name'];
      const positionData = this.props.pbsNodePosition[nodeName].position;
      if (positionData) {
        if (
          nodeMode == 0 &&
          selectedNode.length > 0 &&
          !selectedNode.includes(nodeName)
        ) {
          node.setVisible(false);
          return;
        }
        if (!node.isVisible()) {
          node.setVisible(true);
        }
        node.setPosition(
          scaleFactor * positionData[0],
          scaleFactor * positionData[1]
        );
      } else {
        disabledNode.push(nodeName);
        node.setVisible(false);
      }
    });

    this.setState(oldState => ({
      ...oldState,
      model: currentModel
    }));
    this.autoZoomGraph(50);
  };

  private handleFilterMenuOpen = () => {
    this.setState(oldState => ({ ...oldState, filterMenuToggle: true }));
  };

  private handleFilterMenuClose = (event: any) => {
    const value = event.currentTarget.getAttribute('value');
    this.setState(
      oldState => ({
        ...oldState,
        filterMenuToggle: false,
        filterMode: value
      }),
      this.syncPosition
    );
  };

  render() {
    return (
      <div style={{ height: '100%' }}>
        <div style={{ height: 'calc(100% - 30px)' }}>
          <BaseCanvasWidget>
            <CanvasWidget engine={this.state.engine} />
          </BaseCanvasWidget>
        </div>
        <div style={{ height: '30px', display: 'flex' }}>
          <Button variant="contained" onClick={this.autoDistribute}>
            Auto position
          </Button>
          <Button variant="contained" onClick={this.syncPosition}>
            sync position
          </Button>
          <Button
            variant="contained"
            aria-controls="simple-menu"
            aria-haspopup="true"
            onClick={this.handleFilterMenuOpen}
            ref={this.filterBtnRef}
            startIcon={<SettingsIcon />}
          >
            {FILTER_MODE[this.state.filterMode]}
          </Button>
          <Menu
            id="simple-menu"
            anchorEl={this.filterBtnRef.current}
            keepMounted
            open={this.state.filterMenuToggle}
          >
            <MenuItem value={0} onClick={this.handleFilterMenuClose}>
              Selected nodes
            </MenuItem>
            <MenuItem value={1} onClick={this.handleFilterMenuClose}>
              All nodes
            </MenuItem>
          </Menu>
        </div>
      </div>
    );
  }
}

export default withStyles(styles)(
  connect(mapStateToProps, mapDispatchToProps)(GraphPanel)
);

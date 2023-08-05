/* Copyright 2021 Karlsruhe Institute of Technology
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. */

import Rete from 'rete';
import {v4 as uuidv4} from 'uuid';

import Node from 'scripts/lib/workflows/core/Node.vue';

export const sockets = {
  str: new Rete.Socket('str'),
  int: new Rete.Socket('int'),
  float: new Rete.Socket('float'),
  bool: new Rete.Socket('bool'),
  dep: new Rete.Socket('dep'),
  env: new Rete.Socket('env'),
  stdio: new Rete.Socket('stdio'),
};

export const commonInputs = {
  dep: {key: 'dependency', title: 'Dependencies', socket: sockets.dep, multi: true},
  env: {key: 'env', title: 'env', socket: sockets.env},
  stdio: {key: 'pipe', title: 'stdin', socket: sockets.stdio},
};

export const commonOutputs = {
  dep: {key: 'dependency', title: 'Dependents', socket: sockets.dep, multi: true},
  env: {key: 'env', title: 'env', socket: sockets.env},
  stdio: {key: 'pipe', title: 'stdout', socket: sockets.stdio},
};

const toolInputs = [commonInputs.dep, commonInputs.env, commonInputs.stdio];
const toolInputKeys = toolInputs.map((input) => input.key);
const toolOutputs = [commonOutputs.dep, commonOutputs.env, commonOutputs.stdio];

function makeInput(input) {
  return new Rete.Input(input.key, input.title, input.socket, input.multi || false);
}

function makeOutput(output) {
  return new Rete.Output(output.key, output.title, output.socket, output.multi || false);
}

function makeFlowPort(io, direction, position, index) {
  if (io.param) {
    return {
      name: io.param.name,
      type: io.param.type,
      required: io.param.required,
      shortName: io.param.char,
      port_direction: direction,
      port_index: index,
      position,
    };
  }

  return {
    name: io.name,
    type: io.key,
    required: false,
    shortName: '',
    port_direction: direction,
    port_index: index,
    position: 0,
  };
}

// Not currently used, as choices are not stored in the Flow file.
// eslint-disable-next-line no-unused-vars
function parseChoices(choiceString) {
  const choices = [];
  let choice = '';
  let prevChar = null;

  for (const char of choiceString) {
    if (char === '|' && prevChar !== '\\') {
      choices.push(choice);
      choice = '';
    } else {
      choice += char;
    }

    prevChar = char;
  }

  if (choice) {
    choices.push(choice);
  }

  return choices;
}

class BaseComponent extends Rete.Component {
  constructor(name, type) {
    super(name);
    this.type = type;
    this.data.component = Node;
  }

  /* eslint-disable class-methods-use-this */
  builder(node) {
    // Check whether the node already has a UUID from loading it via a Flow file.
    if (typeof (node.id) === 'number') {
      node.id = `{${uuidv4()}}`;
    }
    return node;
  }

  fromFlow(flowNode) {
    const node = {
      id: flowNode.id,
      name: flowNode.model.name,
      data: {},
      inputs: new Map(),
      outputs: new Map(),
      position: [flowNode.position.x, flowNode.position.y],
    };
    return node;
  }

  toFlow(node) {
    const flowNode = {
      id: node.id,
      model: {name: node.name},
      position: {x: node.position[0], y: node.position[1]},
    };
    return flowNode;
  }
  /* eslint-enable class-methods-use-this */
}

export class BuiltinComponent extends BaseComponent {
  constructor(name, type, menu, inputs = [], outputs = []) {
    super(name, type);
    this.menu = menu;
    this.inputs = inputs;
    this.outputs = outputs;
  }

  builder(node) {
    const _node = super.builder(node);
    _node.type = this.type;

    for (const input of this.inputs) {
      _node.addInput(makeInput(input));
    }
    for (const output of this.outputs) {
      _node.addOutput(makeOutput(output));
    }

    return _node;
  }

  fromFlow(flowNode) {
    const node = super.fromFlow(flowNode);

    for (const input of this.inputs) {
      node.inputs.set(input.key, {connections: []});
    }
    for (const output of this.outputs) {
      node.outputs.set(output.key, {connections: []});
    }

    return node;
  }
}

export class ToolComponent extends BaseComponent {
  constructor(tool) {
    super(ToolComponent.nameFromTool(tool), 'tool');
    this.tool = tool;
  }

  static nameFromTool(tool) {
    if (tool.version !== null) {
      return `${tool.name} ${tool.version}`;
    }

    return tool.name;
  }

  static toolFromFlow(flowNode) {
    const flowTool = flowNode.model.tool;
    const tool = {
      name: flowTool.name,
      path: flowTool.name,
      version: flowTool.version,
      param: [],
    };

    for (const port of flowNode.model.tool.ports) {
      if (!toolInputKeys.includes(port.type)) {
        const param = {
          name: port.name,
          char: port.shortName,
          type: port.type,
          required: port.required,
        };
        tool.param.push(param);
      }
    }

    return tool;
  }

  builder(node) {
    const _node = super.builder(node);
    _node.type = this.type;

    for (const output of toolOutputs) {
      _node.addOutput(makeOutput(output));
    }
    _node.addInput(makeInput(toolInputs[0]));

    for (let i = 0; i < this.tool.param.length; i++) {
      const param = this.tool.param[i];
      const paramName = param.name || `arg${i}`;
      let input = null;

      switch (param.type) {
      case 'string':
        input = new Rete.Input(`in${i}`, `String: ${paramName}`, sockets.str);
        break;
      case 'int':
      case 'long':
        input = new Rete.Input(`in${i}`, `Integer: ${paramName}`, sockets.int);
        break;
      case 'float':
      case 'real':
        input = new Rete.Input(`in${i}`, `Float: ${paramName}`, sockets.float);
        break;
      case 'bool':
      case 'flag':
        input = new Rete.Input(`in${i}`, `Boolean: ${paramName}`, sockets.bool);
        break;
      default:
        input = new Rete.Input(`in${i}`, `${kadi.utils.capitalize(param.type)}: ${paramName}`, sockets.str);
      }

      input.param = {
        name: param.name,
        char: param.char,
        type: param.type,
        required: param.required || false,
      };

      _node.addInput(input);
    }

    for (const input of toolInputs.slice(1)) {
      _node.addInput(makeInput(input));
    }

    return _node;
  }

  // eslint-disable-next-line class-methods-use-this
  fromFlow(flowNode) {
    const node = super.fromFlow(flowNode);
    node.name = ToolComponent.nameFromTool(flowNode.model.tool);

    let inputIndex = 0;
    for (const port of flowNode.model.tool.ports) {
      if (port.port_direction === 'in') {
        if (toolInputKeys.includes(port.type)) {
          node.inputs.set(port.type, {connections: []});
        } else {
          node.inputs.set(`in${inputIndex++}`, {connections: []});
        }
      } else {
        // Tool nodes only use builtin outputs so far.
        node.outputs.set(port.type, {connections: []});
      }
    }

    return node;
  }

  toFlow(node) {
    const flowNode = super.toFlow(node);

    flowNode.model = {
      name: 'ToolNode',
      tool: {
        name: this.tool.name,
        path: this.tool.name,
        version: this.tool.version,
        ports: [],
      },
    };

    let iterator = node.inputs.values();
    let position = 1;

    for (let index = 0; index < node.inputs.size; index++) {
      const input = iterator.next().value;
      const port = makeFlowPort(input, 'in', position++, index);
      flowNode.model.tool.ports.push(port);
    }

    iterator = node.outputs.values();
    position = 1;

    for (let index = 0; index < node.outputs.size; index++) {
      const output = iterator.next().value;
      const port = makeFlowPort(output, 'out', position++, index);
      flowNode.model.tool.ports.push(port);
    }

    return flowNode;
  }
}

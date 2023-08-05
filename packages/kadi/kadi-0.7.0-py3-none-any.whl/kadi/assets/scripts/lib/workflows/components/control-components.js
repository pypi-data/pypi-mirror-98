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

import {sockets, commonInputs, commonOutputs, BuiltinComponent} from 'core';
import PortControl from 'scripts/lib/workflows/controls/port-control';

const type = 'control';
const menu = 'Control';

const variable = new BuiltinComponent(
  'Variable',
  type,
  menu,
  [
    commonInputs.dep,
    {key: 'name', title: 'Name', socket: sockets.str},
    {key: 'value', title: 'Value', socket: sockets.str},
  ],
  [commonOutputs.dep],
);

const ifBranch = new BuiltinComponent(
  'IfBranch',
  type,
  menu,
  [
    commonInputs.dep,
    {key: 'condition', title: 'Condition', socket: sockets.bool},
  ],
  [
    commonOutputs.dep,
    {key: 'true', title: 'True', socket: sockets.dep},
    {key: 'false', title: 'False', socket: sockets.dep},
  ],
);

const loop = new BuiltinComponent(
  'Loop',
  type,
  menu,
  [
    commonInputs.dep,
    {key: 'condition', title: 'Condition', socket: sockets.bool},
    {key: 'startIndex', title: 'Start Index [0]', socket: sockets.int},
    {key: 'endIndex', title: 'End Index', socket: sockets.int},
    {key: 'indexVarName', title: 'Index Variable Name', socket: sockets.str},
  ],
  [
    commonOutputs.dep,
    {key: 'loop', title: 'Loop', socket: sockets.dep},
    {key: 'index', title: 'Index', socket: sockets.int},
  ],
);

class BranchComponent extends BuiltinComponent {
  constructor() {
    super(
      'BranchSelect',
      type,
      menu,
      [commonInputs.dep, {key: 'selected', title: 'Selected', socket: sockets.int}],
      [commonOutputs.dep],
    );
  }

  builder(node) {
    const _node = super.builder(node);

    _node.prevBranches = 0;
    _node.addControl(new PortControl('branches', 'Branches'));

    this.editor.on('controlchanged', (control) => {
      if (control.parent === _node) {
        this.setBranches(_node);
      }
    });

    return _node;
  }

  fromFlow(flowNode) {
    const node = super.fromFlow(flowNode);

    node.data.branches = flowNode.model.nBranches;
    for (let i = 0; i < node.data.branches; i++) {
      node.outputs.set(`branch${i}`, {connections: []});
    }

    return node;
  }

  toFlow(node) {
    const flowNode = super.toFlow(node);
    flowNode.model.nBranches = node.data.branches;
    return flowNode;
  }

  setBranches(node) {
    const branches = node.data.branches;

    if (branches > node.prevBranches) {
      for (let i = node.prevBranches; i < branches; i++) {
        node.addOutput(new Rete.Output(`branch${i}`, `Branch ${i + 1}`, sockets.dep));
      }
    } else {
      for (let i = branches; i < node.prevBranches; i++) {
        const output = node.outputs.get(`branch${i}`);
        for (const connection of output.connections) {
          this.editor.removeConnection(connection);
        }
        node.removeOutput(output);
      }
    }

    node.vueContext.$forceUpdate();
    node.prevBranches = branches;
  }
}

export default [variable, ifBranch, loop, new BranchComponent()];

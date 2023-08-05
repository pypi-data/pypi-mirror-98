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

const type = 'user-input';
const menu = 'User Input';

const inputs = [commonInputs.dep, {key: 'prompt', title: 'Prompt', socket: sockets.str}];
const commonOutputValues = {key: 'value', title: 'Value'};

const userInputText = new BuiltinComponent(
  'UserInputText',
  type,
  menu,
  inputs,
  [commonOutputs.dep, {...commonOutputValues, socket: sockets.str}],
);

const userInputInteger = new BuiltinComponent(
  'UserInputInteger',
  type,
  menu,
  inputs,
  [commonOutputs.dep, {...commonOutputValues, socket: sockets.int}],
);

const userInputFloat = new BuiltinComponent(
  'UserInputFloat',
  type,
  menu,
  inputs,
  [commonOutputs.dep, {...commonOutputValues, socket: sockets.float}],
);

const userInputBool = new BuiltinComponent(
  'UserInputBool',
  type,
  menu,
  inputs,
  [commonOutputs.dep, {...commonOutputValues, socket: sockets.bool}],
);

const userInputFile = new BuiltinComponent(
  'UserInputFile',
  type,
  menu,
  inputs,
  [commonOutputs.dep, {...commonOutputValues, socket: sockets.str}],
);

const userInputCropImages = new BuiltinComponent(
  'UserInputCropImages',
  type,
  menu,
  inputs.concat([{key: 'imagePath', title: 'Image Path', socket: sockets.str}]),
  [commonOutputs.dep, {key: 'cropInfo', title: 'Crop Info', socket: sockets.str}],
);

class ChooseComponent extends BuiltinComponent {
  constructor() {
    super(
      'UserInputChoose',
      type,
      menu,
      inputs,
      [commonOutputs.dep, {key: 'selected', title: 'Selected', socket: sockets.int}],
    );
  }

  builder(node) {
    const _node = super.builder(node);

    _node.addControl(new PortControl('options', 'Options'));
    _node.prevOptions = 0;

    this.editor.on('controlchanged', (control) => {
      if (control.parent === _node) {
        this.setOptions(_node);
      }
    });

    return _node;
  }

  fromFlow(flowNode) {
    const node = super.fromFlow(flowNode);

    node.data.options = flowNode.model.nOptions;
    for (let i = 0; i < node.data.options; i++) {
      node.inputs.set(`option${i}`, {connections: []});
    }

    return node;
  }

  toFlow(node) {
    const flowNode = super.toFlow(node);
    flowNode.model.nOptions = node.data.options;
    return flowNode;
  }

  setOptions(node) {
    const options = node.data.options;

    if (options > node.prevOptions) {
      for (let i = node.prevOptions; i < options; i++) {
        node.addInput(new Rete.Input(`option${i}`, `Option ${i + 1}`, sockets.str));
      }
    } else {
      for (let i = options; i < node.prevOptions; i++) {
        const input = node.inputs.get(`option${i}`);
        for (const connection of input.connections) {
          this.editor.removeConnection(connection);
        }
        node.removeInput(input);
      }
    }

    node.vueContext.$forceUpdate();
    node.prevOptions = options;
  }
}

export default [
  userInputText,
  userInputInteger,
  userInputFloat,
  userInputBool,
  userInputFile,
  userInputCropImages,
  new ChooseComponent(),
];

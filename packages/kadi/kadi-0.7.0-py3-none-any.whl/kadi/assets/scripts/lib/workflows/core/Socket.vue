<!-- Copyright 2020 Karlsruhe Institute of Technology
   -
   - Licensed under the Apache License, Version 2.0 (the "License");
   - you may not use this file except in compliance with the License.
   - You may obtain a copy of the License at
   -
   -     http://www.apache.org/licenses/LICENSE-2.0
   -
   - Unless required by applicable law or agreed to in writing, software
   - distributed under the License is distributed on an "AS IS" BASIS,
   - WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   - See the License for the specific language governing permissions and
   - limitations under the License. -->

<template>
  <div class="socket" :class="[type, socket.name, used ? 'used' : ''] | kebab"></div>
</template>

<script>
import VueRenderPlugin from 'rete-vue-render-plugin';

export default {
  extends: VueRenderPlugin.Socket,
  props: {
    used: Boolean,
  },
};
</script>

<style lang="scss" scoped>
@import 'styles/workflows/workflow-editor.scss';

.socket {
  background: white;
  border: 2px solid $socket-color;
  border-radius: $socket-size / 2.0;
  box-sizing: border-box;
  cursor: pointer;
  display: inline-block;
  height: $socket-size;
  margin: $socket-margin;
  position: relative;
  vertical-align: middle;
  width: $socket-size;
  z-index: 2;

  &.input {
    margin-left: -$socket-size / 2;
  }

  &.output {
    margin-right: -$socket-size / 2;
  }

  &.used {
    background: $socket-color;
    border: 2px solid #c9c9c9;
  }

  &:hover {
    border-width: 4px;
  }

  /* Socket types. */

  &.choice {
    background: #164aab;
  }

  &.bool {
    background: #fa5a5a;
  }

  &.dep {
    background: #72de6d;
  }

  &.env {
    background: #636363;
  }

  &.float {
    background: #77dfed;
  }

  &.int {
    background: #c660fc;
  }

  &.stdio {
    background: #f5f384;
  }

  &.str {
    background: #6b9fff;
  }
}
</style>

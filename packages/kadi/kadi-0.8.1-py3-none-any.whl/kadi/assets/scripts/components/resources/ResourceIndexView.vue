<!-- Copyright 2021 Karlsruhe Institute of Technology
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
  <card-deck :items="resources" :num-cards="2">
    <template #default="props">
      <div class="card-body">
        <a :href="props.item._links.view" class="stretched-link">
          <p>
            <small>
              <i class="fas mr-1"
                 :class="{'fa-lock-open': props.item.visibility === 'public',
                          'fa-lock': props.item.visibility === 'private'}">
              </i>
            </small>
            <strong>{{ props.item.title }}</strong>
            <span class="badge badge-primary type-badge font-weight-normal ml-2" v-if="props.item.type">
              {{ props.item.type }}
            </span>
            <br>
            @{{ props.item.identifier }}
          </p>
          <span class="text-muted" v-if="props.item.plain_description">
            {{ props.item.plain_description | truncate(200) }}
          </span>
          <em class="text-muted" v-else>{{ i18n.t('misc.noDescription') }}</em>
        </a>
      </div>
      <div class="card-footer bg-white py-1">
        <small class="text-muted">
          {{ i18n.t('misc.lastModified') }} <from-now :timestamp="props.item.last_modified"></from-now>
        </small>
      </div>
    </template>
  </card-deck>
</template>

<script>
export default {
  props: {
    resources: Array,
  },
};
</script>

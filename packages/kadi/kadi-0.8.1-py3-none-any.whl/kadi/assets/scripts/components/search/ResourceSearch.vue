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
  <div class="card">
    <div class="card-header py-2">
      <div class="d-flex justify-content-between align-items-center">
        <span v-if="initialized">{{ i18n.t('search.results', {count: total}) }}</span>
        <span v-else>{{ i18n.t('misc.loading') }}</span>
        <i class="fas fa-circle-notch fa-spin" v-if="loading"></i>
      </div>
    </div>
    <div class="card-body results">
      <div class="list-group list-group-flush">
        <div class="list-group-item list-group-item-action text-body" v-for="resource in resources" :key="resource.id">
          <a :href="resource._links.view">
            <div class="row">
              <div class="col-sm-2 d-flex align-items-center mb-2 mb-sm-0" v-if="resource._links.image">
                <img class="img-thumbnail"
                     width="100"
                     :src="resource._links.image + '?ts=' + kadi.utils.timestamp(resource.last_modified)">
              </div>
              <div :class="{'col-sm-10': resource._links.image, 'col-sm-12': !resource._links.image}">
                <div class="row mb-2 mb-sm-0">
                  <div class="col-sm-7">
                    <small>
                      <i class="fas mr-1"
                         :class="{'fa-lock-open': resource.visibility === 'public',
                                  'fa-lock': resource.visibility === 'private'}">
                      </i>
                    </small>
                    <strong>{{ resource.title }}</strong>
                    <span class="badge badge-primary type-badge font-weight-normal ml-2" v-if="resource.type">
                      {{ resource.type }}
                    </span>
                    <p>@{{ resource.identifier }}</p>
                  </div>
                  <div class="col-sm-5 d-sm-flex justify-content-end">
                    <div class="text-sm-right">
                      <small class="text-muted">
                        {{ i18n.t('misc.created') }} <from-now :timestamp="resource.created_at"></from-now>
                      </small>
                      <br>
                      <small class="text-muted">
                        {{ i18n.t('misc.lastModified') }} <from-now :timestamp="resource.last_modified"></from-now>
                      </small>
                    </div>
                  </div>
                </div>
                <div class="text-muted pb-3">
                  <span v-if="resource.plain_description">{{ resource.plain_description | truncate(300) }}</span>
                  <em v-else>No description.</em>
                </div>
                <div class="row align-items-end">
                  <div :class="{'col-sm-9': hasExtras(resource), 'col-sm-12': !hasExtras(resource)}">
                    {{ i18n.t('misc.createdBy') }} <identity-popover :user="resource.creator"></identity-popover>
                  </div>
                  <div class="col-sm-3 mt-2 mt-sm-0 d-flex justify-content-sm-end align-items-end"
                       v-if="hasExtras(resource)">
                    <collapse-item :id="`extras-${resource.id}`" :is-collapsed="true">
                      {{ i18n.t('misc.extras') }}
                    </collapse-item>
                  </div>
                </div>
              </div>
            </div>
          </a>
          <div class="collapse mt-2" :id="`extras-${resource.id}`" v-if="hasExtras(resource)">
            <metadata-viewer :extras="resource.extras"></metadata-viewer>
          </div>
        </div>
        <div class="list-group-item" v-if="!loading && resources.length === 0">
          <em class="text-muted">{{ i18n.t('misc.noResults') }}</em>
        </div>
      </div>
      <div class="border-top justify-content-center" :class="{'d-flex': total > perPage, 'd-none': total <= perPage}">
        <div class="py-3">
          <pagination-control :total="total"
                              :per-page="perPage"
                              :max-pages="100"
                              @update-page="updatePage"
                              ref="pagination">
          </pagination-control>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
  .results {
    padding: 0 0 1px 0;
  }
</style>

<script>
export default {
  data() {
    return {
      resources: [],
      total: 0,
      perPage: 10,
      pageParam: 'page',
      initialized: false,
      loading: false,
    };
  },
  props: {
    endpoint: String,
  },
  methods: {
    hasExtras(resource) {
      return resource.extras && resource.extras.length > 0;
    },
    updatePage(page) {
      const url = kadi.utils.setSearchParam(this.pageParam, page);
      kadi.utils.replaceState(url);
      this.search(false);
    },
    search(removePageParam = true) {
      this.loading = true;

      if (removePageParam) {
        const url = kadi.utils.removeSearchParam(this.pageParam);
        kadi.utils.replaceState(url);
        this.$refs.pagination.setPage(1);
      }

      const paramsObj = {};
      const params = new URLSearchParams(new URL(window.location).search);
      for (const key of params.keys()) {
        paramsObj[key] = params.getAll(key);
      }

      axios.get(this.endpoint, {params: paramsObj})
        .then((response) => {
          const data = response.data;
          this.resources = data.items;
          this.total = data._pagination.total_items;
          this.perPage = Number.parseInt(kadi.utils.getSearchParam('per_page'), 10) || 10;

          if (!this.initialized) {
            this.$refs.pagination.setPage(data._pagination.page);
          }
        })
        .catch((error) => kadi.alert(i18n.t('error.loadData'), {xhr: error.request, scrollTo: false}))
        .finally(() => {
          this.initialized = true;
          this.loading = false;
        });
    },
  },
  mounted() {
    this.search(false);
  },
};
</script>

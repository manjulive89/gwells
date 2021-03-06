/*
Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/
<template>
  <fieldset>
    <b-row>
      <b-col cols="12" lg="6">
        <legend :id="id">Well Development</legend>
      </b-col>
      <b-col cols="12" lg="6">
        <div class="float-right">
          <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">Save</b-btn>
          <back-to-top-link v-if="isStaffEdit"/>
        </div>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="4" lg="3">
        <form-input
            id="developmentMethod"
            label="Development Method"
            select
            :options="codes.development_methods"
            hint="Select one or more methods. Hold the Ctrl (PC) or Command (Mac) key to select more than one option."
            text-field="description"
            value-field="development_method_code"
            v-model="developmentMethodInput"
            :multiple="true"
            :errors="errors['development_method']"
            :loaded="fieldsLoaded['development_method']"></form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="4" lg="2">
        <form-input
            id="developmentHours"
            label="Development Hours"
            type="number"
            v-model="developmentHoursInput"
            :errors="errors['development_hours']"
            :loaded="fieldsLoaded['development_hours']"></form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="10" lg="6">
        <form-input
            id="developmentNotes"
            label="Development Notes"
            v-model="developmentNotesInput"
            :errors="errors['development_notes']"
            :loaded="fieldsLoaded['development_notes']"></form-input>
      </b-col>
    </b-row>
  </fieldset>
</template>

<script>
import { mapGetters } from 'vuex'

import inputBindingsMixin from '@/common/inputBindingsMixin.js'

import BackToTopLink from '@/common/components/BackToTopLink.vue'

export default {
  mixins: [inputBindingsMixin],
  components: {
    BackToTopLink
  },
  props: {
    developmentMethod: Array,
    developmentHours: String,
    developmentNotes: String,
    errors: {
      type: Object,
      default: () => ({})
    },
    fieldsLoaded: {
      type: Object,
      default: () => ({})
    },
    id: {
      type: String,
      isInput: false
    },
    isStaffEdit: {
      type: Boolean,
      isInput: false
    },
    saveDisabled: {
      type: Boolean,
      isInput: false
    }
  },
  fields: {
    developmentMethodInput: 'developmentMethod',
    developmentHoursInput: 'developmentHours',
    developmentNotesInput: 'developmentNotes'

  },
  data () {
    return {}
  },
  computed: {
    ...mapGetters(['codes'])
  }
}
</script>

<style>

</style>

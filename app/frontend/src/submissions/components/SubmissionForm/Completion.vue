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
        <legend :id="id">Well Completion Data</legend>
      </b-col>
      <b-col cols="12" lg="6">
        <div class="float-right">
          <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">Save</b-btn>
          <back-to-top-link v-if="isStaffEdit"/>
        </div>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="6" lg="4">
        <form-input
            id="totalDepthDrilled"
            label="Total Depth Drilled"
            v-model="totalDepthDrilledInput"
            type="number"
            hint="ft"
            :errors="errors['total_depth_drilled']"
            :loaded="fieldsLoaded['total_depth_drilled']">
        </form-input>
      </b-col>
      <b-col cols="12" md="6" lg="4">
        <form-input
            id="finishedWellDepth"
            label="Finished Well Depth"
            v-model="finishedWellDepthInput"
            type="number"
            hint="ft (bgl)"
            :errors="errors['finished_well_depth']"
            :loaded="fieldsLoaded['finished_well_depth']">
        </form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="6" lg="4">
        <form-input
            id="finalCasingStickUp"
            label="Final Casing Stick Up"
            type="number"
            v-model="finalCasingStickUpInput"
            hint="in"
            :errors="errors['final_casing_stick_up']"
            :loaded="fieldsLoaded['final_casing_stick_up']">
        </form-input>
      </b-col>
      <b-col cols="12" md="6" lg="4">
        <form-input
            id="bedrockDepth"
            label="Depth to Bedrock"
            type="number"
            v-model="bedrockDepthInput"
            hint="ft (bgl)"
            :errors="errors['depth_to_bedrock']"
            :loaded="fieldsLoaded['depth_to_bedrock']">
        </form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="6" lg="4">
        <form-input
            id="staticWaterLevel"
            label="Static Water Level"
            v-model="staticWaterLevelInput"
            type="number"
            hint="ft (btoc)"
            :errors="errors['static_water_level']"
            :loaded="fieldsLoaded['static_water_level']">
        </form-input>
      </b-col>
      <b-col cols="12" md="6" lg="4">
        <form-input
            id="wellYield"
            label="Estimated Well Yield"
            type="number"
            v-model="wellYieldInput"
            hint="USgpm"
            :errors="errors['well_yield']"
            :loaded="fieldsLoaded['well_yield']">
        </form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="6" lg="4">
        <form-input
            id="artesianFlow"
            label="Artesian Flow"
            v-model="artesianFlowInput"
            hint="USgpm"
            type="number"
            :errors="errors['artesian_flow']"
            :loaded="fieldsLoaded['artesian_flow']">
        </form-input>
      </b-col>
      <b-col cols="12" md="6" lg="4">
        <form-input
            id="artesianPressure"
            label="Artesian Pressure"
            v-model="artesianPressureInput"
            hint="ft"
            type="number"
            :errors="errors['artesian_pressure']"
            :loaded="fieldsLoaded['artesian_pressure']">
        </form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12" md="6" lg="4">
        <form-input
            id="wellCapType"
            label="Well Cap Type"
            v-model="wellCapTypeInput"
            :errors="errors['well_cap_type']"
            :loaded="fieldsLoaded['well_cap_type']">
        </form-input>
      </b-col>
      <b-col cols="12" md="6" lg="4">
        <b-form-group label="Well Disinfected Status" id="wellDisinfectedStatusInput">
          <b-form-select
            v-model="wellDisinfectedInput"
            value-field="well_disinfected_code"
            text-field="well_disinfected_code"
            :options="disinfected_codes()"
            :errors="errors['well_disinfected_status']"
            :loaded="fieldsLoaded['well_disinfected_status']">
          </b-form-select>
        </b-form-group>
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
    totalDepthDrilled: String,
    finishedWellDepth: String,
    finalCasingStickUp: String,
    bedrockDepth: String,
    staticWaterLevel: String,
    wellYield: String,
    artesianFlow: String,
    artesianPressure: String,
    wellCapType: String,
    wellDisinfected: null,
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
    totalDepthDrilledInput: 'totalDepthDrilled',
    finishedWellDepthInput: 'finishedWellDepth',
    finalCasingStickUpInput: 'finalCasingStickUp',
    bedrockDepthInput: 'bedrockDepth',
    staticWaterLevelInput: 'staticWaterLevel',
    wellYieldInput: 'wellYield',
    artesianFlowInput: 'artesianFlow',
    artesianPressureInput: 'artesianPressure',
    wellCapTypeInput: 'wellCapType',
    wellDisinfectedInput: 'wellDisinfected'
  },
  data () {
    return {}
  },
  methods: {
    disinfected_codes () { // make the unknown selection disabled for users
      if (this.codes != null && this.codes.well_disinfected_codes != null) {
        this.codes.well_disinfected_codes.forEach((code, index, object) => {
          if (code.well_disinfected_code === 'Unknown') {
            if (!this.isStaffEdit) {
              object.splice(index, 1)
            }
          }
        })
        return this.codes.well_disinfected_codes
      }
    }
  },
  computed: {
    ...mapGetters(['codes'])
  }
}
</script>

<style>

</style>

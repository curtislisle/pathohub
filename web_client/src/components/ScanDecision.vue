<script>
import { mapMutations } from 'vuex';
import UserAvatar from './UserAvatar.vue';
import { decisionOptions } from '../constants';

export default {
  name: 'ScanDecision',
  components: {
    UserAvatar,
  },
  props: {
    decision: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      decisionOptions,
    };
  },
  computed: {
    artifactChips() {
      return Object.entries(this.decision.user_identified_artifacts).filter(
        ([, selected]) => selected === 1,
      ).map(
        ([artifactName]) => ({
          code: artifactName.toUpperCase().slice(0, 3),
          value: artifactName.replace(/_/g, ' '),
        }),
      );
    },
  },
  methods: {
    ...mapMutations(['setSliceLocation']),
    convertDecisionToColor(decision) {
      if (decision === 'UN') return 'red--text text--darken-2';
      if (decision === 'U') return 'green--text text--darken-2';
      return 'grey--text text--darken-2';
    },
    goToLocation() {
      this.setSliceLocation(this.decision.location);
    },
  },
};
</script>

<template>
  <v-flex
    class="d-flex"
    style="flex-direction:row; column-gap: 5px; margin-bottom: 10px;"
  >
    <div
      class="d-flex"
      style="flex-direction:row; column-gap: 2px"
    >
      <UserAvatar
        v-if="decision.creator"
        :target-user="decision.creator"
      />
      <div :class="convertDecisionToColor(decision.decision)">
        <v-tooltip bottom>
          <template #activator="{ on, attrs }">
            <span
              v-bind="attrs"
              v-on="on"
            >
              ({{ decision.decision }})
            </span>
          </template>
          <span>{{ decisionOptions[decision.decision] }}</span>
        </v-tooltip>
      </div>
      <v-tooltip bottom>
        <template #activator="{ on, attrs }">
          <v-icon
            v-if="Object.values(decision.location).length > 0"
            v-bind="attrs"
            v-on="on"
            @click="goToLocation"
          >
            mdi-crosshairs-gps
          </v-icon>
        </template>
        <span>View location saved with decision</span>
      </v-tooltip>
    </div>
    <v-flex
      :class="decision.note ? 'black--text' : 'grey--text'"
      class="d-flex justify-space-between"
    >
      {{ decision.note ? decision.note : "No comment" }}
    </v-flex>
    <v-flex
      shrink
      class="d-flex flex-wrap justify-end flex-shrink-1"
    >
      <v-tooltip
        v-for="chip in artifactChips"
        :key="'chip_'+ chip.value"
        :v-bind="chip.code"
        bottom
      >
        <template #activator="{ on, attrs }">
          <v-chip
            v-bind="attrs"
            small
            v-on="on"
          >
            {{ chip.code }}
          </v-chip>
        </template>
        <span>{{ chip.value }}</span>
      </v-tooltip>
    </v-flex>
    <div
      class="grey--text"
      style="text-align: right"
    >
      {{ decision.created }}
    </div>
  </v-flex>
</template>

<style scoped>
.col{
  padding: 0px;
  margin: 0px;
}
</style>

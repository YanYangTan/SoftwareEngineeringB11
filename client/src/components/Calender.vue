<template>
  <v-app id="dayspan" v-cloak>

    <ds-calendar-app ref="app"
      :calendar="calendar"
      :read-only="readOnly"
      @change="saveState">

      <template slot="title">
        DaySpan
      </template>

      <template slot="menuRight">
        <v-btn icon large href="https://github.com/ClickerMonkey/dayspan-vuetify" target="_blank">
          <v-avatar size="32px" tile>
            <img src="https://simpleicons.org/icons/github.svg" alt="Github">
          </v-avatar>
        </v-btn>
      </template>

      <template slot="eventPopover" slot-scope="slotData">
         <ds-calendar-event-popover
          v-bind="slotData"
          :read-only="readOnly"
          @finish="saveState"
        ></ds-calendar-event-popover>
      </template>

      <template slot="eventCreatePopover" slot-scope="{placeholder, calendar}">
        <ds-calendar-event-create-popover
          :calendar-event="placeholder"
          :calendar="calendar"
          :close="$refs.app.$refs.calendar.clearPlaceholder"
          @create-edit="$refs.app.editPlaceholder"
          @create-popover-closed="saveState"
        ></ds-calendar-event-create-popover>
      </template>

      <template slot="eventTimeTitle" slot-scope="{calendarEvent, details}">
        <div>
          <v-icon class="ds-ev-icon"
            v-if="details.icon"
            size="14"
            :style="{color: details.forecolor}">
            {{ details.icon }}
          </v-icon>
          <strong class="ds-ev-title">{{ details.title }}</strong>
        </div>
        <div class="ds-ev-description">{{ getCalendarTime( calendarEvent ) }}</div>
      </template>

      <template slot="drawerBottom">
        <div class="pa-3">
          <v-checkbox
            label="Read Only?"
            v-model="readOnly"
          ></v-checkbox>
        </div>
      </template>

    </ds-calendar-app>

  </v-app>
</template>

<script>
// eslint-disable-next-line import/no-extraneous-dependencies
import { Calendar } from 'dayspan';
import Vue from 'vue';

export default {

  name: 'Calender',
  data: () => ({
    // storeKey: 'dayspanState',
    calendar: Calendar.months(),
    readOnly: false,
    defaultEvents: [

    ],
  }),

  mounted() {
    window.app = this.$refs.app;

    this.loadState();
  },

  methods:
  {
    getCalendarTime(calendarEvent) {
      const sa = calendarEvent.start.format('a');
      const ea = calendarEvent.end.format('a');
      let sh = calendarEvent.start.format('h');
      let eh = calendarEvent.end.format('h');

      if (calendarEvent.start.minute !== 0) {
        sh += calendarEvent.start.format(':mm');
      }

      if (calendarEvent.end.minute !== 0) {
        eh += calendarEvent.end.format(':mm');
      }

      return (sa === ea) ? (`${sh} - ${eh}${ea}`) : (`${sh + sa} - ${eh}${ea}`);
    },

    saveState() {
      const state = this.calendar.toInput(true);
      const json = JSON.stringify(state);

      localStorage.setItem(this.storeKey, json);
    },

    loadState() {
      let state = {};

      try {
        const savedState = JSON.parse(localStorage.getItem(this.storeKey));

        if (savedState) {
          state = savedState;
          state.preferToday = false;
        }
      } catch (e) {
        // eslint-disable-next-line
        console.log( e );
      }

      if (!state.events || !state.events.length) {
        state.events = this.defaultEvents;
      }

      state.events.forEach((ev) => {
        const defaults = this.$dayspan.getDefaultEventDetails();

        // eslint-disable-next-line no-param-reassign
        ev.data = Vue.util.extend(defaults, ev.data);
      });

      this.$refs.app.setState(state);
    },
  },
};
</script>

<style>

body, html, #app, #dayspan {
  font-family: Roboto, sans-serif !important;
  width: 100%;
  height: 50%;
}

</style>

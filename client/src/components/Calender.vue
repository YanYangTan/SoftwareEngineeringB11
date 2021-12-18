<template>
  <v-app id="dayspan" v-cloak>
    <ds-calendar-app ref="app"
      :calendar="calendar"
      :read-only="readOnly"
      v-loading.fullscreen.lock="fullscreenLoading"
      @change="saveState">

      <template slot="title">
        Calendar
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

    </ds-calendar-app>
  </v-app>
</template>

<style>
body, html, #app, #dayspan {
  font-family: Roboto, sans-serif !important;
  width: 100%;
  height: 100%;
}
.v-btn--flat,
.v-text-field--solo .v-input__slot {
  background-color: #f5f5f5 !important;
  margin-bottom: 8px !important;
}
.ds-day-picker{
  transition: all .2s ease-in-out;
  box-shadow: 0 1px 3px grey;
}
.ds-day-picker:hover{
  transform: scale(1.01);
  box-shadow: 0 4px 8px grey;
  background-color: #ffffff;
}
.ds-week-header{
  background-color: #c5ccf2;
}
.mb-2{
  box-shadow: 0 1px #3b3d48;
}
.subtitle{
  color: white;
}
.ds-day{
  background-color: #f1f3fc;
  border: 1px solid #e0e0e0;
}
.ds-week-view-scrollable{
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>

<script>
// eslint-disable-next-line import/no-extraneous-dependencies
import { Calendar } from 'dayspan';
import Vue from 'vue';
// eslint-disable-next-line
import axios from 'axios';

export default {
  name: 'Calender',
  data: () => ({
    // storeKey: 'dayspanState',
    fullscreenLoading: true,
    calendar: Calendar.months(),
    readOnly: false,
    defaultEvents: [],
  }),
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
      const json = JSON.stringify(state.events);
      // Send json to backend
      axios.post('/api/save-calendar', {
        isGroup: this.$route.params.isGroup === '1',
        id: this.$route.params.id,
        content: json,
      })
        .then((res) => {
          if (res.data.status) {
            console.log('Saved');
          } else {
            console.log('Save Failed');
          }
        });
    },
    loadState() {
      this.fullscreenLoading = true;
      const state = {};
      if (!state.events || !state.events.length) {
        state.events = this.defaultEvents;
      }
      state.events.forEach((ev) => {
        const defaults = this.$dayspan.getDefaultEventDetails();
        // eslint-disable-next-line no-param-reassign
        ev.data = Vue.util.extend(defaults, ev.data);
      });
      // Load from backend
      let events = [];
      axios.post('/api/query-calendar', {
        isGroup: this.$route.params.isGroup === '1',
        id: this.$route.params.id,
      })
        .then((res) => {
          if (res.data.status) {
            console.log('Query success!');
            events = res.data.calendar;
            state.events = events;
            this.$refs.app.setState(state);
            console.log(state.events);
            this.fullscreenLoading = false;
          } else {
            console.log(res.data.message);
          }
        });
    },
  },
  mounted() {
    window.app = this.$refs.app;
    this.loadState();
  },
};
</script>

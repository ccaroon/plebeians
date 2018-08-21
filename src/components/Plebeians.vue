<template>
<v-container>
  <Header v-on:searchTextUpdate="searchTextUpdate"></Header>
  <v-expansion-panel focusable expand>
    <v-expansion-panel-content expand-icon="mdi-chevron-down" v-for="(household,hi) in this.directory" :key="hi">
      <div class="headline" slot="header">
        <v-avatar><v-icon>mdi-home</v-icon></v-avatar>
        {{ household.name }} - <span class="grey--text">{{ household.address1 }} {{ household.address2 }}, {{ household.city }} {{ household.state }} {{ household.zip }}</span>
      </div>
      <v-list dense two-line>
        <v-list-tile v-for="(member,mi) in household.members" :key="mi">
          <v-list-tile-avatar><img src="https://dummyimage.com/200x200/000000/04ff00.png"/></v-list-tile-avatar>
          <v-list-tile-content>
            <v-list-tile-title>{{ member.name }} ({{ member.position }})</v-list-tile-title>
            <v-list-tile-sub-title>Birthday: {{ formatBDay(member.birthday) }}</v-list-tile-sub-title>
            <v-list-tile-sub-title>Phone: {{ member.phone }}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-expansion-panel-content>
  </v-expansion-panel>

  <v-footer absolute color="purple lighten-1">
    <v-layout justify-center row>
      <span class="title text-lg-center">Massey's Chapel UMC</span>
    </v-layout>
  </v-footer>
</v-container>
</template>

<script>
// import axios from 'axios'
import Fuse from 'fuse.js'

import Header from './Header.vue'

export default {
  name: 'Plebeians',

  components: {
    Header: Header
  },

  mounted () {
    this.loadDirectory()
    // this.initSearch()
  },

  computed: {},

  methods: {
    formatBDay: function (dateStr) {
      var bDay = 'N/A'
      if (dateStr) {
        var date = new Date(dateStr)
        bDay = (date.getMonth() + 1) + '/' + (date.getDate() + 1)
      }

      return bDay
    },

    searchTextUpdate: function (searchStr) {
      alert(searchStr)
    },

    loadDirectory: function () {
      this.directory = [
        {
          name: 'Caroon',
          address1: '5520 Middleton Road',
          address2: '',
          city: 'Durham',
          state: 'NC',
          zip: '27713',
          members: [{
            name: 'Craig N. Caroon',
            phone: '919-597-0214',
            birthday: '1971-02-19',
            position: 'Husband/Father'
          }, {
            name: 'Cate Caroon',
            phone: '919-610-1713',
            birthday: '1972-08-23',
            position: 'Wife/Mother'
          }, {
            name: 'Nathan Caroon',
            birthday: '1999-08-18',
            position: 'Child'
          }]
        },
        {
          name: 'Kirkpatrick',
          address1: '123 Carolina Lane',
          address2: '',
          city: 'Cary',
          state: 'NC',
          zip: '27606',
          members: [{
            name: 'Rick Kirkpatrick',
            phone: '919-555-1111',
            birthday: '1800-01-07',
            position: 'Husband'
          }, {
            name: 'Kathy Kirkpatrick',
            phone: '919-555-2222',
            birthday: '1800-07-13',
            position: 'Wife'
          }]
        }
      ]
    },

    initSearch: function () {
      this.fuse = new Fuse(this.directory)
    }
  },

  data () {
    return {
      fuse: null,
      directory: []
    }
  }
}
</script>

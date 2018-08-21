<template>
<v-container>
  <v-layout row>
    <Header v-on:searchTextUpdate="searchTextUpdate"></Header>
  </v-layout>

  <v-layout row>
    <v-expansion-panel focusable expand>
      <v-expansion-panel-content expand-icon="mdi-chevron-down" v-for="(household,hi) in this.displayData" :key="hi">
        <div class="headline" slot="header">
          <v-avatar><v-icon>mdi-home</v-icon></v-avatar>
          {{ household.name }} - <span class="title grey--text">{{ household.address1 }} {{ household.address2 }}, {{ household.city }} {{ household.state }} {{ household.zip }}</span>
        </div>
        <v-list dense three-line>
          <v-list-tile v-for="(member,mi) in household.members" :key="mi">
            <v-list-tile-avatar><img src="https://dummyimage.com/200x200/000000/04ff00.png"/></v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title class="body-2"><strong>{{ member.name }} ({{ member.position }})</strong></v-list-tile-title>
              <v-list-tile-sub-title>Birthday: {{ formatBDay(member.birthday) }}</v-list-tile-sub-title>
              <v-list-tile-sub-title>Email: <a v-bind:href="'mailto:' + member.email">{{ member.email }}</a></v-list-tile-sub-title>
              <v-list-tile-sub-title>Phone: {{ member.phone }}</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-layout>

  <!-- <v-layout justify-center row>
    <v-footer fixed color="purple lighten-1">
        <span class="title text-lg-center">Massey's Chapel UMC</span>
    </v-footer>
  </v-layout> -->
</v-container>
</template>

<script>
// import axios from 'axios'
import Fuse from 'fuse.js'
import Header from './Header.vue'

var people = require('../assets/directory.json')

export default {
  name: 'Plebeians',

  components: {
    Header: Header
  },

  mounted () {
    this.loadDirectory()
    this.initSearch()
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
      if (searchStr) {
        this.displayData = this.fuse.search(searchStr)
      } else {
        this.displayData = this.directory
      }
    },

    loadDirectory: function () {
      this.directory = people
    },

    initSearch: function () {
      this.displayData = this.directory
      this.fuse = new Fuse(this.directory, {
        keys: ['name', 'city', 'members.name'],
        threshold: 0.0,
        shouldSort: true
      })
    }
  },

  data () {
    return {
      fuse: null,
      directory: [],
      displayData: []
    }
  }
}
</script>

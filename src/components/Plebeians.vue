<template>
<v-container>
  <v-layout row>
    <Header v-on:searchTextUpdate="searchTextUpdate"></Header>
  </v-layout>

  <v-layout row>
    <v-expansion-panel focusable expand>
      <v-expansion-panel-content expand-icon="mdi-chevron-down" v-for="(household,hi) in this.displayData" :key="hi">
        <div class="headline" slot="header">
          <v-avatar><v-icon>{{ pickAHome(household.name) }}</v-icon></v-avatar>
          {{ household.name }} - <span class="title grey--text">{{ household.address1 }} {{ household.address2 }}, {{ household.city }} {{ household.state }} {{ household.zip }}</span>
        </div>
        <v-layout row>
          <v-flex xs3 v-for="(member,mi) in household.members" :key="mi">
            <FamilyMember
              v-bind:member="member"
            />
          </v-flex>
        </v-layout>
        <v-card v-if="household.notes.length > 0">
          <v-card-title class="subheading">Notes</v-card-title>
          <v-card-text v-html="cleanNote(household.notes.join('\n'))"></v-card-text>
        </v-card>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-layout>

<!--
        <v-list Xdense three-line>
          <v-list-tile v-for="(member,mi) in household.members" :key="mi">
            <v-list-tile-avatar><img :src="'/static/' + (member.photo ? member.photo : 'unknown.jpeg')"/></v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title class="body-2"><strong>{{ member.name }} <span v-if="member.position">({{ member.position }})</span></strong></v-list-tile-title>

            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile>
            <v-list-tile-content>
              <v-list-tile-title>Notes</v-list-tile-title>
              <v-list-tile-sub-title v-for="(note,ni) in household.notes" :key="ni" v-html="cleanNote(note)">
              </v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
-->

  <!-- <v-layout justify-center row>
    <v-footer fixed color="purple lighten-1">
        <span class="title text-lg-center">Massey's Chapel UMC</span>
    </v-footer>
  </v-layout> -->
</v-container>
</template>

<script>
import axios from 'axios'
import Fuse from 'fuse.js'
import FamilyMember from './FamilyMember.vue'
import Header from './Header.vue'

const homeIcons = [
  '', 'home', 'home-account', 'home-circle', 'home-heart', 'home-map-marker', 'home-outline',
  'home-variant', 'home-modern', 'castle'
]

export default {
  name: 'Plebeians',

  components: {
    FamilyMember: FamilyMember,
    Header: Header
  },

  mounted () {
    this.loadDirectory()
  },

  computed: {},

  methods: {

    cleanNote: function (note) {
      return note.replace(/\\n/g, '<br>')
    },

    digitalRoot: function (word) {
      var root = 0

      // Compute value for word based on ASCII codes
      for (var i = 0; i < word.length; i++) {
        root += word.charCodeAt(i)
      }

      // Condense that number (root) down to a single digit
      var newRoot = 0
      while (root > 9) {
        ('' + root).split('').forEach(function (d) {
          newRoot += parseInt(d)
        })
        root = newRoot
        newRoot = 0
      }

      return (root)
    },

    pickAHome: function (name) {
      // var choice = Math.floor(Math.random() * Math.floor(homeIcons.length))
      var choice = this.digitalRoot(name)

      return 'mdi-' + homeIcons[choice]
    },

    searchTextUpdate: function (searchStr) {
      if (searchStr) {
        this.displayData = this.fuse.search(searchStr)
      } else {
        this.displayData = this.directory
      }
    },

    loadDirectory: function () {
      var self = this

      axios.get('/static/directory.json')
        .then(function (response) {
          self.directory = response.data
          self.initSearch()
        })
        .catch(function (err) {
          console.log('Error Loading Directory: ' + err)
        })
    },

    initSearch: function () {
      this.displayData = this.directory
      this.fuse = new Fuse(this.directory, {
        keys: ['name', 'members.name'],
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

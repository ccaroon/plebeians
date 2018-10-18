<template>
<v-container>
  <v-layout row>
    <v-flex><Header v-on:searchTextUpdate="searchTextUpdate"></Header></v-flex>
  </v-layout>

  <v-layout row>
    <v-flex xs12>
      <v-expansion-panel expand v-model="panelControl">
        <v-expansion-panel-content expand-icon="mdi-chevron-down" v-for="(household,hi) in this.displayData" :key="hi">
          <div class="headline" slot="header">
            <v-avatar><v-icon>{{ pickAHome(household.name) }}</v-icon></v-avatar>
            {{ household.name }} - <span class="title grey--text">{{ household.address }}, {{ household.city }} {{ household.state }} {{ household.zip }}</span>
          </div>
          <v-layout row v-for="(item,i) in new Array(Math.ceil(Object.values(household.members).length/membersPerRow))" :key="i">
            <v-flex xs3 v-for="(member,mi) in Object.values(household.members).slice(i*membersPerRow, (i*membersPerRow)+membersPerRow)" :key="i+mi">
              <FamilyMember
                v-bind:member="member"
              />
            </v-flex>
          </v-layout>
          <v-layout row v-if="household.notes && household.notes.length > 0">
            <v-flex xs3 mr-1 v-for="(note, ni) in household.notes" :key="ni">
              <v-card>
                <v-card-title class="pb-1 title yellow darken-1">{{ note.title }}</v-card-title>
                <v-card-text class="pt-1 yellow lighten-1" v-html="formatNote(note)"></v-card-text>
              </v-card>
            </v-flex>
          </v-layout>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-flex>
  </v-layout>

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

    formatNote: function (note) {
      return (note.text.replace(/\\n/g, '<br>'))
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
      var choice = 7 // this.digitalRoot(name)

      return 'mdi-' + homeIcons[choice]
    },

    searchTextUpdate: function (searchStr) {
      if (searchStr) {
        this.displayData = this.fuse.search(searchStr)
      } else {
        // Close all open panels
        this.panelControl = []
        this.displayData = this.directory
      }
    },

    loadDirectory: function () {
      var self = this

      axios.get(this.$config.dataPrefix + '/directory.json')
        .then(function (response) {
          var data = Object.values(response.data)
          self.directory = data.sort(function (a, b) {
            var nameA = a.name.toUpperCase()
            var nameB = b.name.toUpperCase()
            if (nameA < nameB) {
              return -1
            }
            if (nameA > nameB) {
              return 1
            }

            // names must be equal
            return 0
          })
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
      displayData: [],
      panelControl: [],
      membersPerRow: 4
    }
  }
}
</script>

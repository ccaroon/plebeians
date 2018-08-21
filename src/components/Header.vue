<template>
<div>
  <v-toolbar color="teal">
    <v-toolbar-side-icon color="white"><v-icon>mdi-account</v-icon></v-toolbar-side-icon>
    <v-toolbar-title class="white--text">Massey's Chapel UMC - Member Directory</v-toolbar-title>
    <v-flex xs4 offset-xs1>
      <v-toolbar-items>
        <v-icon>mdi-magnify</v-icon>
        <v-text-field
          placeholder="Search"
          v-model="searchText"
          hide-details
          color="black"
          single-line
          @keyup.enter="execSearch">
        </v-text-field>
        <v-btn @click="clearSearch()" icon><v-icon>mdi-close</v-icon></v-btn>
      </v-toolbar-items>
    </v-flex>
  </v-toolbar>
</div>
</template>

<script>
export default {
  name: 'Header',

  methods: {
    clearSearch: function () {
      this.searchText = null
      this.$emit('searchTextUpdate', this.searchText)
    },

    execSearch: function () {
      this.$emit('searchTextUpdate', this.searchText)
    }
  },

  data () {
    return ({
      searchText: null
    })
  }
}
</script>

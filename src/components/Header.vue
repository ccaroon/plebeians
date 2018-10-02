<template>
  <v-toolbar style="background-color:#67E4BE" light dense app fixed>
    <v-btn fab small title="Home" :href="$config.urls.home">
      <v-icon color="">mdi-church</v-icon>
    </v-btn>
    <v-btn fab small title="Member's Area" :href="$config.urls.membersArea">
      <v-icon color="">mdi-folder-lock</v-icon>
    </v-btn>
    <v-btn fab small title="Directory Feedback" :href="'mailto:'+$config.feedbackEmail+'?subject='+$config.organization.abbrev+' Directory Feedback'">
      <v-icon color="">mdi-message-alert</v-icon>
    </v-btn>
    <v-toolbar-title class="black--text">{{ $config.organization.name }} - Member Directory</v-toolbar-title>
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
    },

    goToUrl: function (url) {
      location.href = url
    }
  },

  data () {
    return ({
      searchText: null
    })
  }
}
</script>

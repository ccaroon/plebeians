<template>
  <v-card>
    <v-card-media Xaspect-ratio="4:3">
      <img width="300" height="300" :src="$config.dataPrefix+'/photos/' + (member.photo ? member.photo : 'unknown.jpeg')"/>
    </v-card-media>
    <v-card-title>
      <span class="title">{{ member.name }}</span>
      <v-btn flat icon color="grey" title="Submit Data Correction" :href="'mailto:'+$config.feedbackEmail+'?subject='+$config.organization.abbrev+' Directory - Data Correction: ' + member.name">
        <v-icon>mdi-message-alert-outline</v-icon>
      </v-btn>
    </v-card-title>
    <v-card-text>
      <strong>Birthday:</strong> {{ formatBDay(member.birthday) }}<br>
      <strong>Email:</strong> <a v-bind:href="'mailto:' + member.email">{{ member.email }}</a><br>
      <span v-for="number in formatPhone()" :key="number">
        <strong>Phone:</strong> {{ number }}<br>
      </span>
    </v-card-text>
    <v-card-text>
      <v-chip outline text-color="black" small v-for="(rel, ri) in member.relationships" :key="ri">
        {{ rel }}
      </v-chip>
    </v-card-text>
  </v-card>
</template>

<script>
const monthAbbr = [
  'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
]

export default {
  name: 'FamilyMember',

  props: ['member'],

  methods: {
    formatPhone: function () {
      var data = []
      if (this.member.phone) {
        Object.keys(this.member.phone).forEach(key => {
          data.push(`${this.member.phone[key]} (${key})`)
        })
      }

      return (data)
    },

    formatBDay: function (dateStr) {
      var bDay = 'N/A'
      if (dateStr) {
        var date = new Date(dateStr)
        bDay = monthAbbr[date.getMonth()] + ' ' + (date.getDate() + 1)
      }

      return bDay
    }
  }
}
</script>

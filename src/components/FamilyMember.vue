<template>
  <v-card>
      <v-card-media aspect-ratio="4:3">
        <img :src="'/static/' + (member.photo ? member.photo : 'unknown.jpeg')"/>
      </v-card-media>
     <v-card-title class="title">{{ member.name }}</v-card-title>
     <v-card-text>
      Birthday: {{ formatBDay(member.birthday) }}<br>
      Email: <a v-bind:href="'mailto:' + member.email">{{ member.email }}</a><br>
      Phone: {{ member.phone }}<br>
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

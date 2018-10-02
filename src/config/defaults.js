var config = {
  // Should match `assetsPublicPath` in config/index.js#dev
  staticPrefix: '',

  organization: {
    name: 'Massey\'s Chapel UMC',
    abbrev: 'MCUMC'
  },

  feedbackEmail: 'craig@caroon.org',

  urls: {
    home: 'http://www.masseyschapelumc.org',
    membersArea: 'http://www.masseyschapelumc.org/mcumc-members.html'
  },

  // Computed Settings - Settings based on other settings
  compile: function () {
    this['dataPrefix'] = `${this.staticPrefix}/static/${this.organization.abbrev.toLowerCase()}`
  }
}

module.exports = config

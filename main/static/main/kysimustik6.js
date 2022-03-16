Vue.createApp({
  delimiters: ['[[', ']]'],
  data() {
    return {
      vanusgrupid: [
        { text: 'LAPS 0-2', value: 0},
        { text: 'LAPS 3-8', value: 1},
        { text: 'LAPS 9-15', value: 2},
        { text: 'VPI', value: 3},
      ],
      selectedVanusgrupp: 0,
      options: [
        { text: '---', value: '' },
        { text: 'Jah', value: 'A' },
        { text: 'Ei', value: 'B' },
      ],
      muutumatudSeisundid: [
        { text: 'Seisund0', id: 0},
        { text: 'Seisund1', id: 1},
        { text: 'Seisund2', id: 2},
        { text: 'Seisund3', id: 3},
      ],
      checkedMuutumatudSeisundid: [],
      toggleShowForm: 'yes',
      kysimused: [
        { text: 'Kysimus', score: '' },
        { text: 'Kysimus', score: '' },
        { text: 'Kysimus', score: '' },
        { text: 'Kysimus', score: '' },
        { text: 'Kysimus', score: '' },
      ],
      yldkysimused: [
        'Küsimus?',
        'Küsimus?',
        'Küsimus?',
      ]
    }
  },
  mounted() {
    this.$nextTick(function () {
      // Code that will run only after the
      // entire view has been rendered
      this.selected_vanusgrupp = 0;
    })
  },
  watch: {
    // whenever variables changes, this functions will run
    checkedMuutumatudSeisundid: {
      // deep: true,
      handler(newQuestion, oldQuestion) {
        if (this.checkedMuutumatudSeisundid.length === 0) {
          this.toggleShowForm = 'yes';
        }
      },
    }
  },
  computed: {
    showKysimusVorm() {
      return this.checkedMuutumatudSeisundid.length > 0;
    },
    showKysimustik() {
      return this.toggleShowForm === 'yes';
    }
  }
}).mount('#kysimustik6')

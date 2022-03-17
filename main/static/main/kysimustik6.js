Vue.createApp({
  delimiters: ['[[', ']]'],
  data() {
    return {
      vanusgrupid: [
        { kysimustik: false, text: 'LAPS 0-2', value: 0},
        { kysimustik: true, text: 'LAPS 3-8', value: 1},
        { kysimustik: true, text: 'LAPS 9-15', value: 2},
        { kysimustik: true, text: 'VPI', value: 3},
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
      kysimustik: [],
      vanusgruppideKysimused: {
        0: [],
        1: [
          { text: '3-8 Kysimus', score: '' },
          { text: 'Kysimus', score: '' },
          { text: 'Kysimus', score: '' }
        ],
        2: [
          { text: '9-15 Kysimus', score: '' },
          { text: 'Kysimus', score: '' },
          { text: 'Kysimus', score: '' }
        ],
        3: [
          { text: 'VPI Küsimus', score: '' },
          { text: 'Kysimus', score: '' },
          { text: 'Kysimus', score: '' }
        ]
      },
      yldkysimused: [],
      vanusgruppideYldKysimused: {
        0: [
          { text: '0-2 ÜldKüsimus', score: '' },
          { text: 'Kysimus', score: '' },
          { text: 'Kysimus', score: '' }
        ],
        1: [
          { text: '3-8 ÜldKüsimus', score: '' },
          { text: 'Kysimus', score: '' },
          { text: 'Kysimus', score: '' }
        ],
        2: [
          { text: '9-15 ÜldKüsimus', score: '' },
          { text: 'Kysimus', score: '' },
          { text: 'Kysimus', score: '' }
        ],
        3: [
          { text: 'VPI ÜldKysimus', score: '' },
          { text: 'Kysimus', score: '' },
          { text: 'Kysimus', score: '' }
        ]
      }
    }
  },
  mounted() {
    this.$nextTick(function () {
      // Code that will run only after the
      // entire view has been rendered
      this.selectedVanusgrupp = 0;
      this.kysimustik = this.vanusgruppideKysimused[this.selectedVanusgrupp];
      this.yldkysimused = this.vanusgruppideYldKysimused[this.selectedVanusgrupp];
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
    },
    selectedVanusgrupp: {
      handler(newQuestion, oldQuestion) {
        this.kysimustik = this.vanusgruppideKysimused[this.selectedVanusgrupp];
        this.yldkysimused = this.vanusgruppideYldKysimused[this.selectedVanusgrupp];
      },
    }
  },
  computed: {
    showKysimusVorm() {
      return this.vanusgrupid[this.selectedVanusgrupp].kysimustik && this.checkedMuutumatudSeisundid.length > 0;
    },
    showKysimustik() {
      return this.vanusgrupid[this.selectedVanusgrupp].kysimustik && this.toggleShowForm === 'yes';
    }
  }
}).mount('#kysimustik6')

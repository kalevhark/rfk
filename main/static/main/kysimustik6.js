Vue.createApp({
  delimiters: ['[[', ']]'],
  data() {
    return {
      showBackgroundInfo: false,
      vanusgrupid: [
        { kysimustik: false, text: 'LAPS 0-2', value: 0},
        { kysimustik: true, text: 'LAPS 3-8', value: 1},
        { kysimustik: true, text: 'LAPS 9-15', value: 2},
        { kysimustik: true, text: 'VPI', value: 3},
      ],
      selectedVanusgrupp: 0,
      skaalad: [
        { text: '1-10', skaalaMax: 10, extraKysimus: 4, value: 0},
        { text: '1-5', skaalaMax: 5, extraKysimus: 2, value: 1},
      ],
      selectedSkaala: 0,
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
          { text: '3-8 Kysimus', valdkond: '1.', score: '' },
          { text: 'Kysimus', valdkond: '', score: '' },
          { text: 'Kysimus', valdkond: '', score: '' }
        ],
        2: [
          { text: '9-15 Kysimus', valdkond: '1.', score: '' },
          { text: 'Kysimus', valdkond: '', score: '' },
          { text: 'Kysimus', valdkond: '', score: '' }
        ],
        3: [
          { text: 'VPI Küsimus', valdkond: '1.', score: '' },
          { text: 'Kysimus', valdkond: '', score: '' },
          { text: 'Kysimus', valdkond: '', score: '' }
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
      this.selectedVanusgrupp = 1;
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
    },
    getScore(kysimusIndex) {
      // `this` points to the vm instance
      return function (kysimusIndex) {
        var selected = this.kysimustik[kysimusIndex]['score'];
        var skaalaMax = this.skaalad[this.selectedSkaala]['skaalaMax'];
        if (!selected) {
          return ''
        }
        var result = 4 / skaalaMax * selected
        if (result < 1) {
          return 0
        }
        if (result < 2) {
          return 1
        }
        if (result < 2.76) {
          return 2
        }
        if (result < 3.5) {
          return 3
        }
        if (result >= 3.5) {
          return 4
        }
        return ''
      }
    }
  }
}).mount('#kysimustik6')

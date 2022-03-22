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
      muutumatudSeisundid: [],
      vanusgruppideMuutumatudSeisundid: {
        0: [
          {text: '0-2 seisund', id: 0},
          {text: 'Seisund1', id: 1},
          {text: 'Seisund2', id: 2},
          {text: 'Seisund3', id: 3},
        ],
        1: [
          {text: '3-8 seisund', id: 0},
          {text: 'Seisund1', id: 1},
          {text: 'Seisund2', id: 2},
          {text: 'Seisund3', id: 3},
        ],
        2: [
          {text: '9-15 seisund', id: 0},
          {text: 'Seisund1', id: 1},
          {text: 'Seisund2', id: 2},
          {text: 'Seisund3', id: 3},
        ],
        3: [
          {text: 'Väljakujunenud dementsus', id: 0},
          {text: 'Pahaloomuline kasvaja parimal võimalikul toetusravil', id: 1},
          {text: 'Juhitav hingamine või pidev hapnikravi (va uneapnoe)', id: 2},
          {text: 'Vaimne alaareng (mõõdukas/raske/sügav)', id: 3},
          {text: 'Püsivalt voodihaige', id: 4},
          {text: 'Kurttummus', id: 5},
          {text: 'Mõlema silma pimedus', id: 6},
        ]
      },
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
          { text: 'Kodus liikumisega', valdkond: '1.2.1', score: '' },
          { text: 'Kodust väljas liikumisega', valdkond: '1.2.2', score: '' },
          { text: 'Istumast püsti tõusmisega', valdkond: '1.3.1', score: '' },
          { text: 'Koduste toimetustega hakkama saamisel (näiteks koristamine, toidu valmistamine)', valdkond: '2.4.1', score: '' },
          { text: 'Nägemisega', valdkond: '3.1', score: '' },
          { text: 'Kuulmisega', valdkond: '3.2', score: '' },
          { text: 'Kõnelemisega', valdkond: '3.3', score: '' },
          { text: 'Söömisega', valdkond: '4.3.1', score: '' },
          { text: 'Igapäevategevustega (nt riietumisega, pesemisega, tualetitoimingutega)', valdkond: '4.4.1', score: '' },
          { text: 'Oluliste igapäevategevuste meelespidamisega', valdkond: '5.2.1', score: '' },
          { text: 'Tööl käimisega ja/või huvitegevuses osalemisega', valdkond: '5.3.1', score: '' },
          { text: 'Muutuvate olukordadega kohanemisega (nt igapäeva rutiini muutus)', valdkond: '6.3.1', score: '' },
          { text: 'Lähedaste inimestega lävimisega', valdkond: '7.3.1', score: '' },
          { text: 'Võõrastega lävimisega', valdkond: '7.3.2', score: '' },
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
          { text: 'Nimetage igapäevategevused, mille juures vajate abi?', score: '' },
          { text: 'Kes Teid nende tegevuste juures abistab ja kui sageli?', score: '' },
          { text: 'Kas ja milliseid abivahendeid kasutate? Kas abivahendi(te)st on abi?', score: '' },
          { text: 'Millist abi olete kohalikust omavalitsusest saanud?', score: '' }
        ]
      }
    }
  },
  mounted() {
    this.$nextTick(function () {
      // Code that will run only after the
      // entire view has been rendered
      this.selectedVanusgrupp = 3;
      this.muutumatudSeisundid = this.vanusgruppideMuutumatudSeisundid[this.selectedVanusgrupp];
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
        this.muutumatudSeisundid = this.vanusgruppideMuutumatudSeisundid[this.selectedVanusgrupp];
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

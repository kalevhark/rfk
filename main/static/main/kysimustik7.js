function initialState() {
    return {
      ipAddress: ipAddress,
      showBackgroundInfo: false,
      skaalad: [
        { text: '1-10', skaala: [1,2,3,4,5,6,7,8,9,10], skaalaMax: 10, extraKysimus: 4, value: 0},
        { text: '0-4', skaala: [0,1,2,3,4], skaalaMax: 4, extraKysimus: 2, value: 1},
      ],
      selectedSkaala: selectedSkaala,
      options: [
        { text: '---', value: '' },
        { text: 'Jah', value: 'A' },
        { text: 'Ei', value: 'B' },
      ],
      vanusgrupid: vanusgrupid,
      selectedVanusgrupp: 0,
      muutumatudSeisundidQuestion: '',
      muutumatudSeisundidList: [],
      vanusgruppideMuutumatudSeisundid: vanusgruppideMuutumatudSeisundid,
      checkedMuutumatudSeisundid: [],
      toggleShowForm: 'yes',
      kysimustikQuestion: '',
      kysimustikList: [],
      vanusgruppideKysimused: vanusgruppideKysimused,
      yldkysimused: [],
      vanusgruppideYldKysimused: vanusgruppideYldKysimused,
      feedback: ''
    }
}

Vue.createApp({
  delimiters: ['[[', ']]'],
  data() {
    return initialState()
  },
  mounted() {
    this.$nextTick(function () {
      // Code that will run only after the
      // entire view has been rendered
      this.selectedVanusgrupp = 3;
      this.muutumatudSeisundidQuestion = this.vanusgruppideMuutumatudSeisundid[this.selectedVanusgrupp]['muutumatudSeisundidQuestion'];
      this.muutumatudSeisundidList = this.vanusgruppideMuutumatudSeisundid[this.selectedVanusgrupp]['muutumatudSeisundidList'];
      this.kysimustikQuestion = this.vanusgruppideKysimused[this.selectedVanusgrupp]['vanusgrupiKysimusedQuestion'];
      this.kysimustikList = this.vanusgruppideKysimused[this.selectedVanusgrupp]['vanusgrupiKysimusedList'];
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
        // this.muutumatudSeisundid = this.vanusgruppideMuutumatudSeisundid[this.selectedVanusgrupp];
        this.muutumatudSeisundidQuestion = this.vanusgruppideMuutumatudSeisundid[this.selectedVanusgrupp]['muutumatudSeisundidQuestion'];
        this.muutumatudSeisundidList = this.vanusgruppideMuutumatudSeisundid[this.selectedVanusgrupp]['muutumatudSeisundidList'];
        // this.kysimustik = this.vanusgruppideKysimused[this.selectedVanusgrupp];
        this.kysimustikQuestion = this.vanusgruppideKysimused[this.selectedVanusgrupp]['vanusgrupiKysimusedQuestion'];
        this.kysimustikList = this.vanusgruppideKysimused[this.selectedVanusgrupp]['vanusgrupiKysimusedList'];
        this.yldkysimused = this.vanusgruppideYldKysimused[this.selectedVanusgrupp];
        // this.checkedMuutumatudSeisundid = [];
        // this.toggleShowForm = 'yes';
        this.resetForm();
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
        var selected = this.kysimustikList[kysimusIndex]['score'];
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
  },
  methods: {
    saveFile: function () {
      alert('Faili lisamine pole veel prototüübis võimalik.')
    },
    resetForm: function () {
      var vm = this;
      vm.checkedMuutumatudSeisundid = [];
      vm.toggleShowForm = 'yes';
      // vm.vanusgruppideKysimused = vanusgruppideKysimused;
      // vm.vanusgruppideYldKysimused = vanusgruppideYldKysimused;
      // vm.kysimustik = vm.vanusgruppideKysimused[vm.selectedVanusgrupp];
      // vm.yldkysimused = vm.vanusgruppideYldKysimused[vm.selectedVanusgrupp];
      vm.kysimustikList.forEach((element) => {
        element['score'] = '';
        element['answer'] = '';
      });
      vm.yldkysimused.forEach((element) => {
        element['answer'] = '';
      });
      vm.feedback = '';
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    saveResults: function () {
      var vm = this
      params = {
        ipAddress: vm.ipAddress,
        vanusgrupp: JSON.stringify(vm.vanusgrupid[vm.selectedVanusgrupp]),
        checkedMuutumatudSeisundid: JSON.stringify(vm.checkedMuutumatudSeisundid),
        toggleShowForm: vm.toggleShowForm,
        kysimustikList: JSON.stringify(vm.kysimustikList),
        // vanusgruppideKysimused: JSON.stringify(vm.vanusgruppideKysimused),
        yldkysimused: JSON.stringify(vm.yldkysimused),
        // vanusgruppideYldKysimused: JSON.stringify(vm.vanusgruppideYldKysimused),
        feedback: vm.feedback
      }
      axios.get(urlSaveResults, {params: params})
        .then(function (response) {
          console.log(response.data.filename);
          var btn = document.getElementById('saveButton')
          btn.innerHTML = 'Salvestatud serverisse: ' + response.data.filename;
          btn.classList.add('w3-pale-green');
          setTimeout(function(){
            btn.innerHTML = 'Saada';
            btn.classList.remove('w3-pale-green');
            vm.resetForm();
          }, 3000);
        })
        .catch(function (error) {
          vm.answer = 'Error! Could not reach the API. ' + error
        })
    },
  }
}).mount('#kysimustik7')

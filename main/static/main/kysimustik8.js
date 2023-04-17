function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) === ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) === 0) {
      return c.substring(name.length, c.length);
    }
  }
}

function checkCookieConsent() {
  return getCookie("CookieOK");
}

function setCookie(cname, cvalue, exdays) {
  if (this.checkCookieConsent()) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
  }
}

function deleteCookie(cname) {
  document.cookie = cname + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
}

function initialState() {
    return {
      showDebug: false,
      ipAddress: ipAddress,
      showBackgroundInfo: false,
      skaalad: [
        { text: '1-10', skaala: [1,2,3,4,5,6,7,8,9,10], extraKysimus: 5,
          legend: [
            '1 = piiranguid ega takistusi ei ole',
            '10 = tegevus on võimatu või täielikult takistatud'
          ],
          value: 0
        },
        { text: '0-4', skaala: [0,1,2,3,4], extraKysimus: 2,
          legend: [
            '0 - PIIRANGUID ei ole',
            '1 - KERGE PIIRANG',
            '2 - MÕÕDUKAS PIIRANG',
            '3 - RASKE PIIRANG',
            '4 - TÄIELIK PIIRANG'
          ],
          value: 1},
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
      v6tmetegevusedList: [],
      vanusgruppideV6tmetegevused: vanusgruppideV6tmetegevused,
      kysimustikQuestion: '',
      kysimustikList: [],
      vanusgruppideKysimused: vanusgruppideKysimused,
      yldkysimusedQuestion: '',
      yldkysimusedList: [],
      vanusgruppideYldKysimused: vanusgruppideYldKysimused,
      vanusgruppideFailiTekstid: vanusgruppideFailiTekstid,
      vanusgrupiFailiTekst: '',
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
      // this.selectedVanusgrupp = 3;
      this.selectedVanusgrupp = getCookie('selectedVanusgrupp') || 0;
      this.muutumatudSeisundidQuestion = this.vanusgruppideMuutumatudSeisundid[this.selectedVanusgrupp]['muutumatudSeisundidQuestion'];
      this.muutumatudSeisundidList = this.vanusgruppideMuutumatudSeisundid[this.selectedVanusgrupp]['muutumatudSeisundidList'];
      this.v6tmetegevusedList = this.vanusgruppideV6tmetegevused[this.selectedVanusgrupp]['vanusgrupiV6tmetegevusedList'];
      this.kysimustikQuestion = this.vanusgruppideKysimused[this.selectedVanusgrupp]['vanusgrupiKysimusedQuestion'];
      this.kysimustikList = this.vanusgruppideKysimused[this.selectedVanusgrupp]['vanusgrupiKysimusedList'];
      this.yldkysimusedQuestion = this.vanusgruppideYldKysimused[this.selectedVanusgrupp]['vanusgrupiYldKysimusedQuestion'];
      this.yldkysimusedList = this.vanusgruppideYldKysimused[this.selectedVanusgrupp]['vanusgrupiYldKysimusedList'];
      this.vanusgrupiFailiTekst = this.vanusgruppideFailiTekstid[this.selectedVanusgrupp];
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
        this.muutumatudSeisundidQuestion = this.vanusgruppideMuutumatudSeisundid[this.selectedVanusgrupp]['muutumatudSeisundidQuestion'];
        this.muutumatudSeisundidList = this.vanusgruppideMuutumatudSeisundid[this.selectedVanusgrupp]['muutumatudSeisundidList'];
        this.v6tmetegevusedList = this.vanusgruppideV6tmetegevused[this.selectedVanusgrupp]['vanusgrupiV6tmetegevusedList'];
        this.kysimustikQuestion = this.vanusgruppideKysimused[this.selectedVanusgrupp]['vanusgrupiKysimusedQuestion'];
        this.kysimustikList = this.vanusgruppideKysimused[this.selectedVanusgrupp]['vanusgrupiKysimusedList'];
        this.yldkysimusedQuestion = this.vanusgruppideYldKysimused[this.selectedVanusgrupp]['vanusgrupiYldKysimusedQuestion'];
        this.yldkysimusedList = this.vanusgruppideYldKysimused[this.selectedVanusgrupp]['vanusgrupiYldKysimusedList'];
        this.vanusgrupiFailiTekst = this.vanusgruppideFailiTekstid[this.selectedVanusgrupp];
        setCookie('selectedVanusgrupp', this.selectedVanusgrupp, 365);
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
      vm.yldkysimusedList.forEach((element) => {
        element['answer'] = '';
      });
      vm.feedback = '';
      var divEkspertiis = document.getElementById('ekspertiis')
      divEkspertiis.innerHTML = '';
      var divRFK = document.getElementById('rfkd')
      divRFK.innerHTML = '';
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    refreshEkspertiis: function () {
      var vm = this
      console.log(vm.v6tmetegevusedList);
      params = {
        vanusgrupp: JSON.stringify(vm.vanusgrupid[vm.selectedVanusgrupp]),
        checkedMuutumatudSeisundid: JSON.stringify(vm.checkedMuutumatudSeisundid),
        v6tmetegevusedList: JSON.stringify(vm.v6tmetegevusedList),
        kysimustikList: JSON.stringify(vm.kysimustikList),
        yldkysimusedList: JSON.stringify(vm.yldkysimusedList)
      }
      axios.get(urlRefreshEkspertiis, {params: params})
        .then(function (response) {
          var btn = document.getElementById('refreshEkspertiis')
          btn.innerHTML = 'Värskendame...';
          btn.classList.add('w3-pale-green');
          setTimeout(function(){
            btn.innerHTML = 'Ekspertiis';
            btn.classList.remove('w3-pale-green');
            // vm.resetForm();
          }, 1000);
          var divEkspertiis = document.getElementById('ekspertiis')
          divEkspertiis.innerHTML = response.data.html;
          var divRFK = document.getElementById('rfkd')
          divRFK.innerHTML = response.data.rfk_table;
        })
        .catch(function (error) {
          vm.answer = 'Error! Could not reach the API. ' + error
        })
    },
    saveResults: function () {
      var vm = this
      params = {
        ipAddress: vm.ipAddress,
        vanusgrupp: JSON.stringify(vm.vanusgrupid[vm.selectedVanusgrupp]),
        checkedMuutumatudSeisundid: JSON.stringify(vm.checkedMuutumatudSeisundid),
        toggleShowForm: vm.toggleShowForm,
        kysimustikList: JSON.stringify(vm.kysimustikList),
        yldkysimusedList: JSON.stringify(vm.yldkysimusedList),
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
}).mount('#kysimustik8')

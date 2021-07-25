var mainVM = new Vue({
  el: '#kysimustik2',
  delimiters: ['[[', ']]'],
  data: {
    levelSevere: 3,
    levelExtreme: 4,
    options: [
      { text: 'Pole piirangut', value: 0 },
      { text: 'Kerge piirang', value: 1 },
      { text: 'Mõõdukas piirang', value: 2 },
      { text: 'Raske piirang', value: 3 },
      { text: 'Täielik piirang', value: 4 },
    ],
    questions: {
      disabilities: 'Millise funktsioonihäirega puude raskusastet taotlete?',
      basicActivities: 'Milles piirang peamiselt avaldub?',
      bodyFunctions: 'Mis on piirangu peamine põhjus?',
      extraActivities: 'Palun täpsustage, kas piirang esineb ka:',
      extraQuestion: ['Märkisite täieliku piirangu valdkondades:', 'palun täpsustage']
    },
    disabilities: [
      {
        id: 1, text: 'Liikumine', value: false, rfk: 'd4',
        basicActivities: [
          {id: 1, text: 'Istumine', rfk: 'd4103', value: 0},
          {id: 2, text: 'Püstiasendi säilitamine', rfk: 'd4154', value: 0},
          {id: 3, text: 'Kodus liikumine', rfk: 'd4600', value: 0},
          {id: 4, text: 'Pikkade vahemaade käimine', rfk: 'd4501', value: 0},
          {id: 5, text: 'Kodust ja muudest hoonetest väljaspool liikumine', rfk: 'd4602', value: 0},
          {id: 6, text: 'Jooksmine', rfk: 'd4552', value: 0},
        ],
        bodyFunctions: [
          {id: 7, text: 'Lihasjõu häire', rfk: 'b730', value: 0},
          {id: 8, text: 'Kõnnaku häire', rfk: 'b770', value: 0},
          {id: 9, text: 'Tahtlike liigutuste kontrollimise häire', rfk: 'b760', value: 0},
          {id: 10, text: 'Valu mingis kehaosas', rfk: 'b2801', value: 0},
        ],
        extraActivities: [
          {id: 11, text: 'Tualettruumi toimingud', rfk: 'd530', value: 0},
          {id: 12, text: 'Riietumine', rfk: 'd540', value: 0},
        ],
        extraQuestion: '',
      },
      {
        id: 2, text: 'Nägemine', value: false, rfk: 'd4',
        basicActivities: [
          {id: 1, text: 'Null', rfk: '', value: 0},
        ],
        bodyFunctions: [
          // {id: 1, text: 'Lihasjõu häire', rfk: 'b730', value: 1},
        ],
        extraActivities: [
          // {id: 1, text: 'Tualettruumi toimingud', rfk: 'd530', value: 0},
        ],
        extraQuestion: '',
      },
      {
        id: 3, text: 'Kuulmine', value: false, rfk: 'd4',
        basicActivities: [
          {id: 1, text: 'Null', rfk: '', value: 0},,
        ],
        bodyFunctions: [
          // {id: 1, text: 'Lihasjõu häire', rfk: 'b730', value: 1},
        ],
        extraActivities: [
          // {id: 1, text: 'Tualettruumi toimingud', rfk: 'd530', value: 0},
        ],
        extraQuestion: '',
      },
      {
        id: 4, text: 'Keel-kõne', value: false, rfk: 'd4',
        basicActivities: [
          {id: 1, text: 'Null', rfk: '', value: 0},
        ],
        bodyFunctions: [
          // {id: 1, text: 'Lihasjõu häire', rfk: 'b730', value: 1},
        ],
        extraActivities: [
          // {id: 1, text: 'Tualettruumi toimingud', rfk: 'd530', value: 0},
        ],
        extraQuestion: '',
      },
      {
        id: 5, text: 'Psüühikahäire', value: false, rfk: 'd4',
        basicActivities: [
          {id: 1, text: 'Null', rfk: '', value: 0},
        ],
        bodyFunctions: [
          // {id: 1, text: 'Lihasjõu häire', rfk: 'b730', value: 1},
        ],
        extraActivities: [
          // {id: 1, text: 'Tualettruumi toimingud', rfk: 'd530', value: 0},
        ],
        extraQuestion: '',
      },
      {
        id: 6, text: 'Vaimne alaareng', value: false, rfk: 'd4',
        basicActivities: [
          {id: 1, text: 'Põhioskuste omandamine', rfk: 'd1550', value: 0},
          {id: 2, text: 'Keeruliste oskuste omandamine', rfk: 'd1551', value: 0},
          {id: 3, text: 'Igapäevatoimingute tegemine', rfk: 'd230', value: 0},
          {id: 4, text: 'Oma aktiivsuse reguleerimine', rfk: 'd2303', value: 0},
          {id: 5, text: 'Elemeentaarne inimestevaheline lävimine', rfk: 'd710', value: 0},
          {id: 6, text: 'Stressi ja muude psüühiliste koormustega toimetulek', rfk: 'd240', value: 0},
        ],
        bodyFunctions: [
          {id: 7, text: 'Intellektuaalne areng', rfk: 'b117', value: 0},
          {id: 8, text: 'Vaimse energia tase', rfk: 'b1300', value: 0},
          {id: 9, text: 'Mälufunktsioonid', rfk: 'b144', value: 0},
          {id: 10, text: 'Tähelepanu funktsioonid', rfk: 'b140', value: 0},
        ],
        extraActivities: [
          {id: 11, text: 'Suhtlemisel ja vestlusel', rfk: 'd350', value: 0},
          {id: 12, text: 'Võõrastega kontakteerumisel', rfk: 'd530', value: 0},
        ],
        extraQuestion: '',
      },
      {
        id: 7, text: 'Muu', value: false, rfk: 'd4',
        basicActivities: [
          {id: 1, text: 'Null', rfk: '', value: 0},
        ],
        bodyFunctions: [
          // {id: 1, text: 'Lihasjõu häire', rfk: 'b730', value: 1},
        ],
        extraActivities: [
          // {id: 1, text: 'Tualettruumi toimingud', rfk: 'd530', value: 0},
        ],
        extraQuestion: '',
      },
    ],
    results: null,
  },
  created: function () {
    // _.debounce is a function provided by lodash to limit how
    // often a particularly expensive operation can be run.
    // In this case, we want to limit how often we access
    // yesno.wtf/api, waiting until the user has completely
    // finished typing before making the ajax request. To learn
    // more about the _.debounce function (and its cousin
    // _.throttle), visit: https://lodash.com/docs#debounce
    this.debouncedGetKysimustik2Results = _.debounce(this.getKysimustik2Results, 500);
    // this.results = this.disabilities.map(
    //   function(disability) {
    //     return {
    //       id: disability.id,
    //       rfk_set: null
    //     }
    //   }
    // )
  },
  computed: {
    checkedDisabilities: function () {
      let array = this.disabilities
      return array.filter(disability => disability.value === true);
    }
  },
  watch: {
    // whenever variables changes, this functions will run
    checkedDisabilities: {
      deep: true,
      handler(newQuestion, oldQuestion) {
        this.debouncedGetKysimustik2Results()
      },
    },
  },
  methods: {
    showBodyFunctions: function (disability) {
      let array = disability.basicActivities;
      return array && Math.max.apply(Math, array.map(function(o) { return o.value; }));
    },
    showExtraActivities: function (disability) {
      let array = disability.bodyFunctions;
      return array && Math.max.apply(Math, array.map(function(o) { return o.value; }));
    },
    showExtraQuestion: function (disability) {
      let arrayBasicActivities = disability.basicActivities;
      let arrayExtraActivities = disability.extraActivities;
      return (
        (
          arrayBasicActivities &&
          Math.max.apply(Math, arrayBasicActivities.map(function(o) { return o.value; }))===this.levelExtreme
        ) ||
        (
          arrayExtraActivities &&
          Math.max.apply(Math, arrayExtraActivities.map(function(o) { return o.value; }))===this.levelExtreme
        )
      );
    },
    listFullRestrictions: function (disability) {
      let arrayBasicActivities = disability.basicActivities;
      let arrayExtraActivities = disability.extraActivities;
      let array = arrayBasicActivities ? arrayBasicActivities.concat(arrayExtraActivities) : arrayExtraActivities;
      return array && array.filter(basicActivity => basicActivity.value === this.levelExtreme);
    },
    getKysimustik2Results: function () {
      var vm = this;
      var url = urlGetKysimustik2Results;
      params = {
        content: JSON.stringify(vm.checkedDisabilities)
      }
      axios.get(url, {params: params})
        .then(function (response) {
          // console.log(response);
          vm.results = response.data.rfk_sets;
        }
      )
        .catch(function (error) {
          console.log(error);
          // vm.answer = 'Error! Could not reach the API. ' + error;
        }
      )
    }
  }
})
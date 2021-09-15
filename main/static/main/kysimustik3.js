var mainVM = new Vue({
  el: '#kysimustik',
  delimiters: ['[[', ']]'],
  data: {
    levelSevere: 3,
    levelExtreme: 4,
    levelTTa: 9,
    options: {
      'restrictions': [
        // { text: '', value: 9 },
        { text: 'Pole piirangut', value: 0 },
        { text: 'Kerge piirang', value: 1 },
        { text: 'Mõõdukas piirang', value: 2 },
        { text: 'Raske piirang', value: 3 },
        { text: 'Täielik piirang', value: 4 },
      ],
      'impairments': [
        // { text: '', value: 9 },
        { text: 'Pole häiret', value: 0 },
        { text: 'Kerge häire', value: 1 },
        { text: 'Mõõdukas häire', value: 2 },
        { text: 'Raske häire', value: 3 },
        { text: 'Täielik häire', value: 4 },
      ],
    },
    questions: {
      disabilities: 'Millises valdkonnas Teil igapäevases elus probleeme esineb?',
      basicActivities:  ['Märkiste probleemi valdkonnas', 'Milles see avaldub või mis seda põhjustab?'],
      description: 'Kas tahate midagi lisada selgituseks?',
    },
    description: '', // kasutaja kirjeldus probleemide kohta
    disabilities: [
      {
        id: 1, text: 'Liikumine', value: false, rfk: 'd4',
        basicActivities: [
          {
            id: 1, text: 'Kui palju suudate kõndida raskusteta:', rfk: 'd450', value: 0,
            options: [
              // { text: '', value: 9 },
              { text: 'Üle kilomeetri', value: 0 },
              { text: 'Ühe kilomeetri', value: 1 },
              { text: 'Pool kilomeetrit', value: 2 },
              { text: '100 meetrit', value: 3 },
              { text: 'Ei saa üldse kõndida', value: 4 },
            ]
          },
          {
            id: 2, text: 'Kas liikumisraskused on seotud liigeste ja luude funktsiooni häirega?', rfk: 'b710-729', value: 0,
            options: [
              // { text: '', value: 9 },
              { text: 'Ei', value: 0 },
              // { text: 'Vastus 1', value: 1 },
              { text: 'Mõõdukalt', value: 2 },
              // { text: 'Vastus 3', value: 3 },
              { text: 'Täielikult ei lase liikuda', value: 4 },
            ]
          },
          {
            id: 3, text: 'Kas liikumisraskused on seotud lihaste funktsiooni häirega?', rfk: 'b730-b749', value: 0,
            options: [
              // { text: '', value: 9 },
              { text: 'Ei', value: 0 },
              // { text: 'Vastus 1', value: 1 },
              { text: 'Mõõdukalt', value: 2 },
              // { text: 'Vastus 3', value: 3 },
              { text: 'Täielikult ei lase liikuda', value: 4 },
            ]
          },
        ],
        extraQuestion: '',
      },
      {
        id: 2, text: 'Käeline tegevus. Enesehooldus', value: false, rfk: 'd4',
        basicActivities: [
          // {
          //   id: 1, text: 'Kehaasendi muutmise ja säilitamise piirang', rfk: 'd410-d429', value: 0,
          //   options: [
              // { text: '', value: 9 },
          //     { text: 'Vastus 0', value: 0 },
          //     { text: 'Vastus 1', value: 1 },
          //     { text: 'Vastus 2', value: 2 },
          //     { text: 'Vastus 3', value: 3 },
          //     { text: 'Vastus 4', value: 4 },
          //   ]
          // },
          {
            id: 2, text: 'Kas esemete kandmine või käsitsemine on raskendatud?', rfk: 'd430-d449', value: 0,
            options: [
              // { text: '', value: 9 },
              { text: 'Ei ole', value: 0 },
              { text: 'Natuke', value: 1 },
              { text: 'Mõõdukalt', value: 2 },
              { text: 'Jah, väga tihti', value: 3 },
              { text: 'Ei ole üldse võimalik', value: 4 },
            ]
          },
          {
            id: 3, text: 'Kas käeline tegevus on põhjustatud liigutuste funktsiooni häirega?', rfk: 'b750-b789', value: 0,
            options: [
              { text: 'Nii ja naa', value: 9 },
              { text: 'Ei', value: 0 },
              // { text: 'Vastus 1', value: 1 },
              // { text: 'Vastus 2', value: 2 },
              { text: 'See on oluline põhjus', value: 3 },
              { text: 'Jah, selle tõttu on käeline tegevus täielikult võimatu', value: 4 },
            ]
          },
        ],
        extraQuestion: '',
      },
      {
        id: 3, text: 'Teadmiste edastamine ja vastuvõtmine. Suhtlemine', value: false, rfk: 'd4',
        basicActivities: [
          {
            id: 1, text: 'Kas teie nägemine on', rfk: 'b210', value: 0,
            options: [
              // { text: '', value: 9 },
              { text: 'Väga hea', value: 0 },
              { text: 'Pigem hea', value: 1 },
              { text: 'Keskpärane', value: 2 },
              { text: 'Väga halb', value: 3 },
              { text: 'Ma ei näe üldse', value: 4 },
            ]
          },
          {id: 2, text: 'Kas teie kuulmine on', rfk: 'b230', value: 0,
            options: [
              // { text: '', value: 9 },
              { text: 'Väga hea', value: 0 },
              { text: 'Pigem hea', value: 1 },
              { text: 'Keskpärane', value: 2 },
              { text: 'Väga halb', value: 3 },
              { text: 'Ma ei näe üldse', value: 4 },
            ]
          },
          {id: 3, text: 'Kas teil on probleem kõnelemisega?', rfk: 'b3', value: 0,
            options: [
              // { text: '', value: 9 },
              { text: 'Kõne on ladus', value: 0 },
              { text: 'Natuke ', value: 1 },
              { text: 'Saan kõneleda väikeste raskustega', value: 2 },
              { text: 'Kõnelemine on väga raske', value: 3 },
              { text: 'Ei saa üldse kõneleda', value: 4 },
            ]
          },
        ],
        extraQuestion: '',
      },
      {
        id: 4, text: 'Vaimne tervis', value: false, rfk: 'd4',
        basicActivities: [
          {
            id: 1, text: 'Kas on probleeme põhioskuste omandamisel?', rfk: 'd1550', value: 0,
            options: [
              // { text: '', value: 9 },
              { text: 'Ei ole', value: 0 },
              { text: 'Natuke', value: 1 },
              { text: 'Mõõdukalt', value: 2 },
              { text: 'Jah, väga tihti', value: 3 },
              { text: 'Ei suuda üldse', value: 4 },
            ]
          },
          {
            id: 2, text: 'Kas on probleeme enesevalitsemisel?', rfk: 'b152', value: 0,
            options: [
              // { text: '', value: 9 },
              { text: 'Ei ole', value: 0 },
              { text: 'Natuke', value: 1 },
              { text: 'Mõõdukalt', value: 2 },
              { text: 'Jah, väga tihti', value: 3 },
              { text: 'Ei suuda üldse ennast valitseda', value: 4 },
            ]
          },
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
    this.debouncedGetKysimustikResults = _.debounce(this.getKysimustikResults, 500);
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
        this.debouncedGetKysimustikResults()
      },
    },
  },
  methods: {
    showBodyFunctions: function (disability) {
      let array = disability.basicActivities;
      array = array.filter(function(o) { if (o.value !== this.levelTTa) {return o; } });
      return array && Math.max.apply(Math, array.map(function(o) { return o.value; })) >= levelSevere;
    },
    getKysimustikResults: function () {
      var vm = this;
      var url = urlGetKysimustikResults;
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
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
            id: 1, text: 'Kõndimise ja liikumise piirang', rfk: 'd450-d469', value: 0,
            options: [
              // { text: '', value: 9 },
              { text: 'Vastus 0', value: 0 },
              { text: 'Vastus 1', value: 1 },
              { text: 'Vastus 2', value: 2 },
              { text: 'Vastus 3', value: 3 },
              { text: 'Vastus 4', value: 4 },
            ]
          },
          {
            id: 2, text: 'Liigeste ja luude funktsiooni häire', rfk: 'b710-b729', value: 0,
            options: [
              // { text: '', value: 9 },
              { text: 'Vastus 0', value: 0 },
              { text: 'Vastus 1', value: 1 },
              { text: 'Vastus 2', value: 2 },
              { text: 'Vastus 3', value: 3 },
              { text: 'Vastus 4', value: 4 },
            ]
          },
          {
            id: 3, text: 'Lihaste funktsiooni häire', rfk: 'b730-b749', value: 0,
            options: [
              // { text: '', value: 9 },
              { text: 'Vastus 0', value: 0 },
              { text: 'Vastus 1', value: 1 },
              { text: 'Vastus 2', value: 2 },
              { text: 'Vastus 3', value: 3 },
              { text: 'Vastus 4', value: 4 },
            ]
          },
        ],
        extraQuestion: '',
      },
      {
        id: 2, text: 'Käeline tegevus. Enesehooldus', value: false, rfk: 'd4',
        basicActivities: [
          {
            id: 1, text: 'Kehaasendi muutmise ja säilitamise piirang', rfk: 'd410-d429', value: 0,
            options: [
              // { text: '', value: 9 },
              { text: 'Vastus 0', value: 0 },
              { text: 'Vastus 1', value: 1 },
              { text: 'Vastus 2', value: 2 },
              { text: 'Vastus 3', value: 3 },
              { text: 'Vastus 4', value: 4 },
            ]
          },
          {
            id: 2, text: 'Esemete kandmise, liigutamise ja käsitsemise piirang', rfk: 'd430-d449', value: 0,
            options: [
              // { text: '', value: 9 },
              { text: 'Vastus 0', value: 0 },
              { text: 'Vastus 1', value: 1 },
              { text: 'Vastus 2', value: 2 },
              { text: 'Vastus 3', value: 3 },
              { text: 'Vastus 4', value: 4 },
            ]
          },
          {
            id: 3, text: 'Liigutuste funktsiooni häire', rfk: 'b750-b789', value: 0,
            options: [
              // { text: '', value: 9 },
              { text: 'Vastus 0', value: 0 },
              { text: 'Vastus 1', value: 1 },
              { text: 'Vastus 2', value: 2 },
              { text: 'Vastus 3', value: 3 },
              { text: 'Vastus 4', value: 4 },
            ]
          },
        ],
        extraQuestion: '',
      },
      {
        id: 3, text: 'Suhtlemine', value: false, rfk: 'd4',
        basicActivities: [
          {
            id: 1, text: 'Nägemine', rfk: 'b210-b229', value: 0,
            options: [
              // { text: '', value: 9 },
              { text: 'Vastus 0', value: 0 },
              { text: 'Vastus 1', value: 1 },
              { text: 'Vastus 2', value: 2 },
              { text: 'Vastus 3', value: 3 },
              { text: 'Vastus 4', value: 4 },
            ]
          },
          {id: 2, text: 'Kuulmine', rfk: 'b230-b249', value: 0,
            options: [
              // { text: '', value: 9 },
              { text: 'Vastus 0', value: 0 },
              { text: 'Vastus 1', value: 1 },
              { text: 'Vastus 2', value: 2 },
              { text: 'Vastus 3', value: 3 },
              { text: 'Vastus 4', value: 4 },
            ]
          },
          {id: 3, text: 'Keel-kõne', rfk: 'b3', value: 0,
            options: [
              // { text: '', value: 9 },
              { text: 'Vastus 0', value: 0 },
              { text: 'Vastus 1', value: 1 },
              { text: 'Vastus 2', value: 2 },
              { text: 'Vastus 3', value: 3 },
              { text: 'Vastus 4', value: 4 },
            ]
          },
        ],
        extraQuestion: '',
      },
      {
        id: 4, text: 'Vaimne tervis', value: false, rfk: 'd4',
        basicActivities: [
          {
            id: 1, text: 'Põhioskuste omandamine', rfk: 'd1550', value: 0,
            options: [
              // { text: '', value: 9 },
              { text: 'Vastus 0', value: 0 },
              { text: 'Vastus 1', value: 1 },
              { text: 'Vastus 2', value: 2 },
              { text: 'Vastus 3', value: 3 },
              { text: 'Vastus 4', value: 4 },
            ]
          },
          {
            id: 2, text: 'Keeruliste oskuste omandamine', rfk: 'd1551', value: 0,
            options: [
              // { text: '', value: 9 },
              { text: 'Vastus 0', value: 0 },
              { text: 'Vastus 1', value: 1 },
              { text: 'Vastus 2', value: 2 },
              { text: 'Vastus 3', value: 3 },
              { text: 'Vastus 4', value: 4 },
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
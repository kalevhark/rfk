Vue.createApp({
    // el: '#watch-example',
    delimiters: ['[[', ']]'],
    data() {
      return {
        rfkCode: '',
        rfkPath: '',
        rfkCodeVerbose: '',
        answer: 'Pole veel midagi otsida...',
      }
    },
    watch: {
        rfkCode: {
            handler(newQuestion, oldQuestion) {
                this.rfkPath = 'Ootan kuni lõpetad trükkimise...'
                this.rfkCodeVerbose = ''
                this.debouncedGetRFKPath();
                this.debouncedGetICFCodeVerbose();
            },
        },
    },
    created: function () {
        // _.debounce is a function provided by lodash to limit how
        // often a particularly expensive operation can be run.
        // In this case, we want to limit how often we access
        // yesno.wtf/api, waiting until the user has completely
        // finished typing before making the ajax request. To learn
        // more about the _.debounce function (and its cousin
        // _.throttle), visit: https://lodash.com/docs#debounce
        this.debouncedGetRFKPath = _.debounce(this.getRFKPath, 500);
        this.debouncedGetICFCodeVerbose = _.debounce(this.getICFCodeVerbose, 500)
    },
    methods: {
      getRFKPath: function () {
        if (this.rfkCode.length < 1) {
          this.rfkPath = ''
          return
        }
        this.rfkPath = 'Otsime...'
        var vm = this
        axios.get(urlICFMatches + '?q=' + encodeURIComponent(vm.rfkCode))
          .then(function (response) {
            if ( response.data ) {
              vm.rfkPath = response.data.result
            } else {
              vm.rfkPath = vm.result + ': sellist koodi ei ole'
            }
          })
          .catch(function (error) {
            vm.rfkPath = 'Error! Could not reach the API. ' + error
          })
      },
      getICFCodeVerbose: function () {
        if (this.rfkCode.length < 1) {
          this.rfkCodeVerbose = ''
          return
        }
        this.rfkCodeVerbose = ''
        var vm = this
        axios.get(urlICFCodeVerbose + '?code=' + encodeURIComponent(vm.rfkCode))
          .then(function (response) {
            if ( response.data ) {
              vm.rfkCodeVerbose = response.data.result
            } else {
              vm.rfkCodeVerbose = 'sellist koodi ei ole'
            }
          })
          .catch(function (error) {
            vm.rfkCodeVerbose = 'Error! Could not reach the API. ' + error
          })
      },
      resetForm: function () {
        location.reload();
      }
    },
}).mount('#codesearch')
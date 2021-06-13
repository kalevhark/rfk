var mainVM = new Vue({
    el: '#watch-example',
    delimiters: ['[[', ']]'],
    data: {
        rfkCode: '',
        rfkPath: '',
        rfkSummary: '',
        resultSummary0: '',
        // resultSummary1: '',
        resultSummary2: '',
        resultSummary3: '',
        answer: 'Pole midagi analüüsida...',
        inputs: [
            {id: 1, question: '', result1: '', result2: '', result3: ''},
            {id: 2, question: '', result1: '', result2: '', result3: ''},
            {id: 3, question: '', result1: '', result2: '', result3: ''},
        ]
    },
    watch: {
        // whenever variables changes, this functions will run
        inputs: {
            deep: true,
            handler(newQuestion, oldQuestion) {
                this.answer = 'Ootan kuni lõpetad trükkimise...'
                this.debouncedGetTables()
            },
        },
        rfkCode: {
            handler(newQuestion, oldQuestion) {
                this.rfkPath = 'Ootan kuni lõpetad trükkimise...'
                this.debouncedGetRFKPath()
            },
        },
        rfkSummary: {
            handler(newQuestion, oldQuestion) {
                // this.rfkPath = 'Ootan kuni lõpetad trükkimise...'
                this.debouncedGetRFKSummary()
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
        this.debouncedGetTables = _.debounce(this.getTables, 500)
        this.debouncedGetRFKPath = _.debounce(this.getRFKPath, 500)
        this.debouncedGetRFKSummary = _.debounce(this.getRFKSummary, 500)
    },
    methods: {
          getRFKPath: function () {
            if (this.rfkCode.length < 1) {
            this.rfkPath = ''
            return
          }
          this.rfkPath = 'Otsime...'
          var vm = this
          axios.get('/main/get_icf_path/?code=' + vm.rfkCode)
            .then(function (response) {
                if ( response.data ) {
                    vm.rfkPath = response.data.rfkPath
                } else {
                    vm.rfkPath = this.rfkCode + ': sellist koodi ei ole'
                }
            })
            .catch(function (error) {
              vm.rfkPath = 'Error! Could not reach the API. ' + error
            })
        },
        getTables: function () {
            var b = this.inputs
            var arr = Object.keys( b ).map( function ( key ) { return b[key].question.length });
            var max = Math.max.apply( null, arr );
            if (max < 3) {
                this.answer = 'Questions are longer. ;-)'
                for (const property in this.inputs) {
                    this.inputs[property].result1 = ''
                    this.inputs[property].result2 = ''
                    this.inputs[property].result3 = ''
                }
                return
            }
            this.answer = 'Arvutame...'
            var vm = this
            for (const property in vm.inputs) {
                if (vm.inputs[property].question.length > 3) {
                    axios.get('/main/get_icf_calcs/?content=' + JSON.stringify(vm.inputs[property].question))
                        .then(function (response) {
                            vm.inputs[property].result1 = response.data.icf_table_matrix_level1
                            vm.inputs[property].result2 = response.data.icf_table_matrix_level2
                            vm.inputs[property].result3 = response.data.icf_table_matrix_level3
                            var b = vm.inputs
                            var arr_question = Object.keys( b ).map( function ( key ) { return b[key].question });
                            vm.answer = arr_question.join(' ')
                            vm.rfkSummary = arr_question.join(' ')
                        })
                        .catch(function (error) {
                            vm.inputs[property].result1 = ''
                            vm.inputs[property].result2 = ''
                            vm.inputs[property].result3 = ''
                            vm.answer = 'Error! Could not reach the API. ' + error
                        })
                    } else {
                        vm.inputs[property].result1 = ''
                        vm.inputs[property].result2 = ''
                        vm.inputs[property].result3 = ''
                    }
            }
        },
        getRFKSummary: function () {
            var vm = this
            console.log(vm.rfkSummary)
            axios.get('/main/get_icf_summary/?content=' + JSON.stringify(vm.rfkSummary))
                .then(function (response) {
                    vm.resultSummary0 = response.data.icf_table_matrix_level0
                    vm.resultSummary2 = response.data.icf_table_matrix_level2
                    vm.resultSummary3 = response.data.icf_table_matrix_level3
                })
                .catch(function (error) {
                    vm.answer = 'Error! Could not reach the API. ' + error
                })
        }
    }
})
var mainVM = new Vue({
    el: '#watch-example',
    delimiters: ['[[', ']]'],
    data: {
        rfkCode: '',
        rfkPath: '',
        selected: 1,
        options: [
          { text: 'Aritmeetiline keskmine', value: 1 },
          { text: 'Ruutkeskmine', value: 2 },
          { text: 'Geomeetriline keskmine (0-määraja->1)', value: 3 },
          { text: 'Geomeetriline keskmine (0-määrajaid ignoreeritakse)', value: 4 },
        ],
        rfkSummary: '',
        resultSummary0: '',
        // resultSummary1: '',
        resultSummary2: '',
        resultSummary3: '',
        resultVerbose2: '',
        answer: 'Pole veel midagi analüüsida...',
        inputs: [
            {id: 1, category: 'Liikumine', question: '', result1: '', result2: '', result3: '', len: 0},
            {id: 2, category: 'Nägemine', question: '', result1: '', result2: '', result3: '', len: 0},
            {id: 3, category: 'Kuulmine', question: '', result1: '', result2: '', result3: '', len: 0},
            {id: 4, category: 'Keel ja kõne', question: '', result1: '', result2: '', result3: '', len: 0},
            {id: 5, category: 'Vaimne', question: '', result1: '', result2: '', result3: '', len: 0},
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
        selected: {
            handler(newQuestion, oldQuestion) {
                this.getTables()
                this.getRFKSummary()
            },
        }
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
        openTab: function (evt, tabName) {
            // console.log(tabName)
            var i, x, tablinks;
            x = document.getElementsByClassName("tab");
            for (i = 0; i < x.length; i++) {
                x[i].style.display = "none";
            }
            tablinks = document.getElementsByClassName("tablink");
            for (i = 0; i < x.length; i++) {
                tablinks[i].className = tablinks[i].className.replace(" w3-red", "");
            }
            document.getElementById(tabName).style.display = "block";
            evt.currentTarget.className += " w3-red";
        },
        getRFKPath: function () {
            if (this.rfkCode.length < 1) {
            this.rfkPath = ''
            return
          }
          this.rfkPath = 'Otsime...'
          var vm = this
          axios.get(urlICFPath + '?code=' + vm.rfkCode)
            .then(function (response) {
                if ( response.data ) {
                    vm.rfkPath = response.data.rfkPath
                } else {
                    vm.rfkPath = vm.rfkCode + ': sellist koodi ei ole'
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
                this.answer = 'Lisa andmeid, et midagi analüüsida...'
                this.resultSummary0 = ''
                this.resultSummary1 = ''
                this.resultSummary2 = ''
                this.resultSummary3 = ''
                this.resultVerbose2 = ''
                for (const property in this.inputs) {
                    this.inputs[property].result1 = ''
                    this.inputs[property].result2 = ''
                    this.inputs[property].result3 = ''
                    this.inputs[property].len = 0
                }
                return
            }
            this.answer = 'Arvutame...'
            var vm = this
            for (const property in vm.inputs) {
                if (vm.inputs[property].question.length > 3) {
                    params = {
                        method: vm.selected,
                        content: JSON.stringify(vm.inputs[property].question)
                    }
                    // var querystring = ['?method=' + method, 'content=' + content].join('&')
                    axios.get(urlICFCalcs, {params: params}) // '?content=' + JSON.stringify(vm.inputs[property].question))
                        .then(function (response) {
                            vm.inputs[property].result1 = response.data.icf_table_matrix_level1
                            vm.inputs[property].result2 = response.data.icf_table_matrix_level2
                            vm.inputs[property].result3 = response.data.icf_table_matrix_level3
                            vm.inputs[property].len = response.data.rfk_codeset_count
                            var b = vm.inputs
                            var arr_question = Object.keys( b ).map( function ( key ) { return b[key].question });
                            vm.answer = arr_question.join(' ')
                            vm.rfkSummary = arr_question.join(' ')
                        })
                        .catch(function (error) {
                            vm.inputs[property].result1 = ''
                            vm.inputs[property].result2 = ''
                            vm.inputs[property].result3 = ''
                            vm.inputs[property].len = 0
                            vm.answer = 'Error! Could not reach the API. ' + error
                        })
                    } else {
                        vm.inputs[property].result1 = ''
                        vm.inputs[property].result2 = ''
                        vm.inputs[property].result3 = ''
                        this.inputs[property].len = 0
                    }
            }
        },
        getRFKSummary: function () {
            var vm = this
            params = {
                method: vm.selected,
                content: JSON.stringify(vm.rfkSummary)
            }
            axios.get(urlICFSummary, {params: params})
                .then(function (response) {
                    vm.resultSummary0 = response.data.icf_table_matrix_level0
                    vm.resultSummary2 = response.data.icf_table_matrix_level2
                    vm.resultSummary3 = response.data.icf_table_matrix_level3
                    vm.resultVerbose2 = response.data.icf_table_verbose_level2
                })
                .catch(function (error) {
                    vm.answer = 'Error! Could not reach the API. ' + error
                })
        },
        makeDemo: function () {
            this.rfkCode = 'b230'
            this.inputs[0].question = 'b28011.3\n' +
                'd4104.2\n' +
                'd4501.3\n' +
                's6302.3\n' +
                's4301.3\n' +
                'd4154.2\n' +
                'd8451.4\n' +
                'b4402.2\n' +
                'b4551.3\n' +
                'b4552.2\n' +
                'b28014.2'
            this.inputs[1].question = 'd4452.3\n' +
                'd430.3\n' +
                's6302.3\n' +
                's4201.3\n' +
                's4301.3\n' +
                'b4552.2'
        }
    }
})
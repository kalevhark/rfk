Vue.createApp({
    // el: '#watch-example',
    delimiters: ['[[', ']]'],
    data() {
        return {
            rfkCode: '',
            rfkPath: '',
            selected: 1,
            options: [
                {text: 'Aritmeetiline keskmine', value: 1},
                {text: 'Ruutkeskmine', value: 2},
                {text: 'Geomeetriline keskmine (0-määraja->1)', value: 3},
                {text: 'Geomeetriline keskmine (0-määrajaid ignoreeritakse)', value: 4},
            ],
            rfkSummary: '',
            resultSummary0: '',
            // resultSummary1: '',
            resultSummary2: '',
            resultSummary3: '',
            resultVerbose2: '',
            resultVerbose3: '',
            resultVerbose4: '',
            answer: 'Pole veel midagi analüüsida...',
            inputs: [
                {id: 1, category: 'Liikumine', question: '', result1: '', result2: '', result3: '', len: 0},
                {id: 2, category: 'Käeline tegevus', question: '', result1: '', result2: '', result3: '', len: 0},
                {id: 3, category: 'Suhtlemine', question: '', result1: '', result2: '', result3: '', len: 0},
                {id: 4, category: 'Enesehooldus', question: '', result1: '', result2: '', result3: '', len: 0},
                {id: 5, category: 'Õppimine', question: '', result1: '', result2: '', result3: '', len: 0},
                {id: 6, category: 'Muutused', question: '', result1: '', result2: '', result3: '', len: 0},
                {id: 7, category: 'Suhted', question: '', result1: '', result2: '', result3: '', len: 0},
            ],
            prt_categories: [
                {
                    id: 1, category: 'Liikumine',
                    tvh_categories: [1], rfk_set: '',
                    result1: '', result2: '', result3: '', len: 0,
                    resultVerbose4: ''
                },
                {
                    id: 2, category: 'Käeline tegevus ja enesehooldus',
                    tvh_categories: [2, 4], rfk_set: '',
                    result1: '', result2: '', result3: '', len: 0,
                    resultVerbose4: ''
                },
                {
                    id: 3, category: 'Nägemine',
                    tvh_categories: [3], rfk_set: '',
                    result1: '', result2: '', result3: '', len: 0,
                    resultVerbose4: ''
                },
                {
                    id: 4, category: 'Kuulmine',
                    tvh_categories: [3], rfk_set: '',
                    result1: '', result2: '', result3: '', len: 0,
                    resultVerbose4: ''
                },
                {
                    id: 5, category: 'Keel-kõne',
                    tvh_categories: [3], rfk_set: '',
                    result1: '', result2: '', result3: '', len: 0,
                    resultVerbose4: ''
                },
                {
                    id: 6, category: 'Vaimne',
                    tvh_categories: [5, 6, 7], rfk_set: '',
                    result1: '', result2: '', result3: '', len: 0,
                    resultVerbose4: ''
                },
            ]
        }
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
        this.debouncedGetTables = _.debounce(this.getTables, 500);
        this.debouncedGetRFKPath = _.debounce(this.getRFKPath, 500);
        this.debouncedGetRFKSummary = _.debounce(this.getRFKSummary, 500);
    },
    mounted: function () {
        document.getElementById('tvh_button_1').className += " w3-pale-green";
        document.getElementById('prt_button_1').className += " w3-pale-green";
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
                tablinks[i].className = tablinks[i].className.replace(" w3-pale-green", "");
            }
            document.getElementById(tabName).style.display = "block";
            evt.currentTarget.className += " w3-pale-green";
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
                this.resultVerbose3 = ''
                this.resultVerbose4 = ''
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
            // TVH maatriksite arvutamine
            for (const property in vm.inputs) {
                if (vm.inputs[property].question.length > 3) {
                    params = {
                        method: vm.selected,
                        content: JSON.stringify(vm.inputs[property].question)
                    }
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
            // PRT maatriksite arvutamine
            for (const prt_category of vm.prt_categories) {
                prt_category.rfk_set = '';
                for (const tvh_category of vm.inputs) {
                    if (tvh_category.question && prt_category.tvh_categories.includes(tvh_category.id)) {
                        prt_category.rfk_set += ('\n' + tvh_category.question);
                    }
                }
                if (prt_category.rfk_set.length > 3) {
                    params = {
                        method: vm.selected,
                        content: JSON.stringify(prt_category.rfk_set)
                    }
                    axios.get(urlICFCalcs, {params: params}) // '?content=' + JSON.stringify(vm.inputs[property].question))
                        .then(function (response) {
                            prt_category.result1 = response.data.icf_table_matrix_level1
                            prt_category.result2 = response.data.icf_table_matrix_level2
                            prt_category.result3 = response.data.icf_table_matrix_level3
                            prt_category.resultVerbose4 = response.data.icf_table_verbose_level4
                            prt_category.len = response.data.rfk_codeset_count
                        })
                        .catch(function (error) {
                            prt_category.result1 = ''
                            prt_category.result2 = ''
                            prt_category.result3 = ''
                            prt_category.resultVerbose4 = ''
                            prt_category.len = 0
                            // vm.answer = 'Error! Could not reach the API. ' + error
                        })
                    } else {
                        prt_category.result1 = ''
                        prt_category.result2 = ''
                        prt_category.result3 = ''
                        prt_category.resultVerbose4 = ''
                        prt_category.len = 0
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
                    vm.resultVerbose3 = response.data.icf_table_verbose_level3
                    vm.resultVerbose4 = response.data.icf_table_verbose_level4
                })
                .catch(function (error) {
                    vm.answer = 'Error! Could not reach the API. ' + error
                })
        },
        makeDemo1: function () {
            this.rfkCode = 'd450'
            for (input of this.inputs) {
                input.question = ''
            }
            this.inputs[0].question = 'b28011.3\n' +
                'd4104.2\n' +
                'd4501.3\n' +
                's6302.3\n' +
                's4301.3\n' +
                'd4154.2\n' +
                'b4402.2\n' +
                'b4551.3\n' +
                'b4552.2\n' +
                'b28014.2'
        },
        makeDemo2: function () {
            this.rfkCode = 'b210'
            for (input of this.inputs) {
                input.question = ''
            }
            this.inputs[2].question = 'd350.3\n' +
                'd138.3\n' +
                'd310.2\n' +
                'b210.2'
        },
        makeDemo3: function () {
            this.rfkCode = 'b230'
            for (input of this.inputs) {
                input.question = ''
            }
            this.inputs[2].question = 'd350.3\n' +
                'd138.3\n' +
                'd310.3\n' +
                'b230.2'
        },
        makeDemo4: function () {
            this.rfkCode = 'b330'
            for (input of this.inputs) {
                input.question = ''
            }
            this.inputs[2].question = 'd350.3\n' +
                'd138.2\n' +
                'd310.1\n' +
                'b330.2'
        },
        makeDemo5: function () {
            this.rfkCode = 'b152'
            for (input of this.inputs) {
                input.question = ''
            }
            this.inputs[4].question = 'd230.3\n' +
                'b152.2\n' +
                'b130.2\n' +
                'd175.3\n' +
                'd160.3\n' +
                'd155.2'
            this.inputs[5].question = 'd240.3\n' +
                'b152.2\n' +
                'b126.2\n' +
                'd175.3\n' +
                'd230.3\n' +
                'b164.2'
            this.inputs[6].question = 'd730.3\n' +
                'b152.2\n' +
                'b130.2\n' +
                'd720.3\n' +
                'b126.3\n'
        },
        makeDemo6: function () {
            this.rfkCode = 'd460'
            for (input of this.inputs) {
                input.question = ''
            }
            this.inputs[0].question = 'd460.3'
        },
        makeDemo7: function () {
            this.rfkCode = 'd460'
            for (input of this.inputs) {
                input.question = ''
            }
            this.inputs[0].question = 'd460.3\n' + 'd450.3\n' +
                'b28015.3\n' +
                's7502.261\n'
        },
        makeDemo8: function () {
            this.rfkCode = 'd460'
            for (input of this.inputs) {
                input.question = ''
            }
            this.inputs[0].question = 'd460.3\n' + 'd450.3\n' +
                'b28011.2\n' +
                'b4552.2\n' +
                's4100.2\n'
        },
        makeDemo9: function () {
            this.rfkCode = 'd460'
            for (input of this.inputs) {
                input.question = ''
            }
            this.inputs[0].question = 'd460.3\n' + 'b210.4\n' + 's220.323\n'
            this.inputs[2].question = 'd110.4\n' + 'b210.4\n' + 's220.323\n'
        },
        makeDemo10: function () {
            this.rfkCode = 'd460'
            for (input of this.inputs) {
                input.question = ''
            }
            this.inputs[0].question = 'd460.3\n'
            this.inputs[6].question =  'b1141.3\n' + 'b117.3\n'
        }
    }
}).mount('#watch-example')
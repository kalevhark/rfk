Vue.createApp({
  delimiters: ['[[', ']]'],
  data() {
    return {
      picked: ['','','','','','','','','','','','','','','','','',''],
      show: false,
      selected: '',
      valdkonnad: [
        [
          'Liikumine',
          [
            [
              'Liikumine eri tasapindadel',
              [
                // ['Küsimus 1', ''], ['Küsimus 2', ''], ['Küsimus 3', '']
              ]
            ],
            [
              'Ohutu ja takistusteta ringiliikumine',
              [
                ['Kodus toa piires ringi liikumisel?', ''], ['Kodust väljas käimisel?', '']
              ]
            ],
            [
              'Seismine ja istumine',
              [
                ['Istumast püsti tõusmisel?', ''],
              ]
            ],
          ]
        ],
        [
          'Käeline tegevus',
          [
            [
              'Käte sirutamine',
              [
                // ['Küsimus 1', ''], ['Küsimus 2', ''], ['Küsimus 3', '']
              ]
            ],
            [
              'Asjade ülestõstmine ja liigutamine',
              [
                // ['Küsimus 1', ''], ['Küsimus 2', '']
              ]
            ],
            [
              'Käteosavus',
              [
                // ['Küsimus 1', ''], ['Küsimus 2', '']
              ]
            ],
            [
              'Muud käelise tegevuse piirangud',
              [
                ['Koduste toimetustega hakkama saamisel?', '']
              ]
            ]
          ],
        ],
        [
          'Suhtlemine',
          [
            [
              'Nägemine',
              [
                // ['Küsimus 1', ''], ['Küsimus 2', ''], ['Küsimus 3', '']
              ]
            ],
            [
              'Kuulmine',
              [
                // ['Küsimus 1', ''], ['Küsimus 2', '']
              ]
            ],
            [
              'Kõnelemine',
              [
                // ['Küsimus 1', ''], ['Küsimus 2', '']
              ]
            ],
            [
              'Teiste inimestega suhtlemine',
              [
                ['Suhtluse alustamisel ja vestluses osalemisel?', ''],
              ]
            ]
          ],
        ],
        [
          'Teadvusel püsimine ja enesehooldus',
          [
            [
              'Teadvusel püsimine ärkveloleku ajal',
              [
                // ['Küsimus 1', ''], ['Küsimus 2', ''], ['Küsimus 3', '']
              ]
            ],
            [
              'Soole ja põie kontrollimine',
              [
                // ['Küsimus 1', ''], ['Küsimus 2', '']
              ]
            ],
            [
              'Söömine ja joomine',
              [
                ['Söömisel?', '']
              ]
            ],
            [
              'Muud teadvusel püsimise ja enesehoolduse piirangud',
              [
                // ['Üle keha pesemisel?', ''],
                // ['Riietumisel?', ''],
                ['Igapäevategevustel (nt riietumisel, pesemisel, tualetitoimingutel)?', ''],
                ['Paar päeva järjest iseseisvalt hakkama saamisel?', ''],
              ]
            ]
          ],
        ],
        [
          'Õppimine ja tegevuste elluviimine',
          [
            [
              'Tegevuste õppimine',
              [
                // ['Küsimus 1', ''], ['Küsimus 2', ''], ['Küsimus 3', '']
              ]
            ],
            [
              'Tegevuste alustamine ja lõpetamine',
              [
                ['Oluliste tegemiste meeldejätmisega?', '']
              ]
            ],
            [
              'Muud õppimise ja tegevuste elluviimise piirangud',
              [
                ['Lasteaias/koolis/tööl käimisega?', '']
              ]
            ]
          ],
        ],
        [
          'Muutustega kohanemine ja ohu tajumine',
          [
            [
              'Väljaskäimine',
              [
                // ['Küsimus 1', ''], ['Küsimus 2', ''], ['Küsimus 3', '']
              ]
            ],
            [
              'Ohu tajumine',
              [
                // ['Küsimus 1', ''], ['Küsimus 2', '']
              ]
            ],
            [
              'Toimetulek muutustega',
              [
                ['Igapäevaelu korraldamisel ja tegevustega hakkama saamisel?', '']
              ]
            ]
          ],
        ],
        [
          'Inimestevaheline lävimine ja suhted',
          [
            [
              'Sotsiaalsete olukordadega hakkamasaamine',
              [
                // ['Küsimus 1', ''], ['Küsimus 2', ''], ['Küsimus 3', '']
              ]
            ],
            [
              'Olukorrale kohane käitumine',
              [
                // ['Küsimus 1', ''], ['Küsimus 2', '']
              ]
            ],
            [
              'Muud inimestevahelise lävimise ja suhete piirangud',
              [
                ['Suhtlemisel inimestega, keda te ei tunne?', ''], ['Lähedaste inimestega läbisaamisel?', '']
              ]
            ]
          ],
        ]
      ],
      options: [
        { text: '---', value: '' },
        { text: 'Jah', value: 'A' },
        { text: 'Ei', value: 'B' },
      ],
      yldkysimused: [
        'Kirjeldage oma sõnadega, millist abi ja hoolitsust vajate terviseseisundi tõttu enam võrreldes teiste eakaaslastega?',
        'Kui sageli olete kogenud takistusi ja piiranguid ümbritseva keskkonna tõttu?',
        'Kui palju on olnud lähedastel probleeme teie terviseseisundi tõttu?<br>Kas lähedased on pidanud teie terviseseisundi tõttu pidanud elukorraldust muutma?',
      ]
    }
  },
  computed: {
    score1(n) {
      // `this` points to the vm instance
      return n => Math.round(4/10*this.picked[n])
    },
    score2(n) {
      // `this` points to the vm instance
      return function (n) {
        if (!this.picked[n]) {
          return ''
        }
        var result = 4/10*this.picked[n]
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
    },
    score2_uus(valdkondIndex, v6tmetegevusIndex, kysimusIndex) {
      // `this` points to the vm instance
      return function (valdkondIndex, v6tmetegevusIndex, kysimusIndex) {
        var selected = this.valdkonnad[valdkondIndex][1][v6tmetegevusIndex][1][kysimusIndex][1]
        if (!selected) {
          return ''
        }
        var result = 4/10*selected
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
    },
    score3(n) {
      // `this` points to the vm instance
      return function (n) {
        if (!this.picked[n]) {
          return ''
        }
        var result = this.picked[n] / 10 * 100
        if (result <= 5) {
          return 0
        }
        if (result < 25) {
          return 1
        }
        if (result < 50) {
          return 2
        }
        if (result < 95) {
          return 3
        }
        if (result >= 95) {
          return 4
        }
        return ''
      }
    },
    simplified() {
      return this.selected === 'A'
    }
  }
}).mount('#kysimustik4')

Vue.createApp({
  delimiters: ['[[', ']]'],
  data() {
    return {
      picked: ['','','','','','','','','','','','','','','','','',''],
      show: true,
      selected: '',
      valdkonnad: [
        [
          'Liikumine',
          [
            [
              'Võtmevaldkond 1',
              [
                ['Küsimus 1', ''], ['Küsimus 2', ''], ['Küsimus 3', '']
              ]
            ],
            [
              'Võtmevaldkond 2',
              [
                ['Küsimus 1', ''], ['Küsimus 2', '']
              ]
            ],
            [
              'Võtmevaldkond 3',
              [
                ['Küsimus 1', ''], ['Küsimus 2', ''], ['Küsimus 3', '']
              ]
            ],
          ]
        ],
        [
          'Käeline tegevus ja enesehooldus',
          [
            [
              'Võtmevaldkond 1',
              [
                ['Küsimus 1', ''], ['Küsimus 2', ''], ['Küsimus 3', '']
              ]
            ],
            [
              'Võtmevaldkond 2',
              [
                ['Küsimus 1', ''], ['Küsimus 2', '']
              ]
            ],
          ],
        ]
      ],
      options: [
        { text: '---', value: '' },
        { text: 'Jah', value: 'A' },
        { text: 'Ei', value: 'B' },
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
        if (result < 2) {
          return 0
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
        if (result < 2) {
          return 0
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

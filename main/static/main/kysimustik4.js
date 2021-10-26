Vue.createApp({
  delimiters: ['[[', ']]'],
  data() {
    return {
      picked: ['','','','','','','','','','','','','','','','','',''],
      show: true
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
    score3(n) {
      // `this` points to the vm instance
      return function (n) {
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
    }
  }
}).mount('#kysimustik4')

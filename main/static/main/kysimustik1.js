var mainVM = new Vue({
  el: '#kysimustik1',
  delimiters: ['[[', ']]'],
  data: {
    categoriesLevel1:
      [
        { text: 'Liikumine', value: 1, valdkond: 'd4' },
        { text: 'Nägemine', value: 2, valdkond: 'd3' },
        { text: 'Kuulmine', value: 3, valdkond: 'd3' },
        { text: 'Keel-kõne', value: 4, valdkond: 'd3' },
        { text: 'Psüühikahäire', value: 5, valdkond: 'd2' },
        { text: 'Vaimne alaareng', value: 6, valdkond: 'd2' },
        { text: 'Muu', value: 7, valdkond: 'd5' },
      ],
    checkedCategoriesLevel1: [],
    selectedCategoriesLevel1: null
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
      // evt.currentTarget.className += " w3-red";
      this.selectedCategoriesLevel1 = Number(tabName.split()[1])
    },
  },
  watch: {
    // whenever variables changes, this functions will run
    checkedCategoriesLevel1: {
      deep: true,
      handler(newQuestion, oldQuestion) {
        this.selectedCategoriesLevel1 = checkedCategoriesLevel1[-1].value ? checkedCategoriesLevel1 : null
        this.openTab(none, 'valdkond_' + this.selectedCategoriesLevel1)
      },
    },
  }
})
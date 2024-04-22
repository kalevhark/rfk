function openCity(evt, cityName) {
  var i, x, tablinks;
  x = document.getElementsByClassName("city");
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].classList.remove('w3-red');
  }
  var y = document.getElementsByClassName("code_" + cityName);
  for (i = 0; i < y.length; i++) {
    y[i].style.display = "block";
  }
  evt.currentTarget.classList.add('w3-red');
}

function checkCodes() {
  let decks = document.querySelectorAll(".results_on_deck");
  decks.forEach(
    (deck) => {
      let code = deck.id.split('_', 1)[0];
      let m22raja = document.getElementById(code + "_activities").value;
      if (m22raja !== '---' && deck.hasChildNodes() !== true) {
        document.getElementById(code + "_kategooria_text").classList.add('invalid');
      } else {
        document.getElementById(code + "_kategooria_text").classList.remove('invalid');
      }
    }
  );
}

function kontrolli(elementId) {
  var outerDiv = document.getElementById(elementId + "_kategooria_on_deck");
  let items = outerDiv.childNodes.length;
  if (items > 0) {
    let childNode = outerDiv.childNodes[items - 1];
    let childNodeTextSplits = childNode.textContent.trim().split(' ');
    let childNodeText = childNodeTextSplits[1].trim();
    if (childNodeText.includes('.') === false) {
      // console.log('viga!');
      document.getElementById(elementId + "_kategooria_text").value = childNodeText + '.';
      $(childNode).find('span').trigger( "click" );
    } else {
      checkCodes();
    }
  }
}

// function eemalda(elementId) {
  // collectCodes();
// }

window.onload = (event) => {
  let decks = document.querySelectorAll(".results_on_deck");
  decks.forEach(
    (deck) => {
      let elementId = deck.id.split('_', 1)[0];
      let element = $("#" + elementId + "_kategooria_on_deck");
      element.bind('added', function() {
        kontrolli(elementId);
      });
      // element.bind('killed', function() {
      //   eemalda(elementId);
      // });
    }
  );
};

const { createApp, ref } = Vue

createApp({
  delimiters: ['[[', ']]'],
  methods: {
    collectCodes: function () {
      let decks = document.querySelectorAll(".results_on_deck");
      let codeset = [];
      decks.forEach(
        (deck) => {
          let code = deck.id.split('_', 1)[0];
          let m22raja = $("#" + code + "_activities")[0].value;
          if (m22raja !== '---' && deck.hasChildNodes()) {
            let children = deck.childNodes;
            for (const node of children) {
              codeset.push([code + "." + m22raja, node.textContent.split(' ')[1]]);
            }
          }
        }
      );
      return JSON.stringify(codeset);
    },
    saveResults: function () {
      var vm = this
      var codeset = vm.collectCodes();
      params = {
        params: codeset
      }
      axios.get(urlGetICFCalcsPRT, {params: params})
        .then(function (response) {
          var btn = document.getElementById('saveButton')
          btn.innerHTML = 'Arvutame...';
          btn.classList.add('w3-pale-green');
          setTimeout(function(){
            btn.innerHTML = 'Arvuta';
            btn.classList.remove('w3-pale-green');
          }, 1000);
          if ( response.data ) {
            // console.log(response.data);
            document.getElementById('db_level1_matrix').innerHTML = response.data.db_level1_matrix;
            document.getElementById('b_level2_matrix').innerHTML = response.data.b_level2_matrix;
          }
        })
        .catch(function (error) {
          vm.answer = 'Error! Could not reach the API. ' + error
        })
      },
    },
  }
).mount('#app')
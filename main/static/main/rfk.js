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

// Linkide kopeerimine lõikelauale
// button onclick="getLinkCopy(this)" onmouseout="outLinkCopy()"
function getLinkCopy(btn) {
  var linkCopyUrl = btn.getAttribute("data-uri");
  var linkCopyId = btn.getAttribute("id");
  // navigator.clipboard.writeText(linkCopyUrl);
  unsecuredCopyToClipboard(linkCopyUrl);
  var tooltip = document.getElementById("linkCopyTooltip_"+linkCopyId);
  if (tooltip !== null) {
    var tooltipInnerHTMLOld = tooltip.innerHTML;
    tooltip.classList.add("w3-pale-green");
    tooltip.innerHTML = "kopeeritud lõikelauale";
    setTimeout(function () {
      tooltip.innerHTML = tooltipInnerHTMLOld;
      tooltip.classList.remove("w3-pale-green");
    }, 2500);
  }
}

function outLinkCopy() {
  var tooltip = document.getElementById("linkCopyTooltip");
  tooltip.classList.remove("w3-pale-green");
  tooltip.innerHTML = "kopeeri link";
}

function unsecuredCopyToClipboard(text) {
  const textArea = document.createElement("textarea");
  textArea.value = text;
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();
  try {
    document.execCommand('copy');
  } catch (err) {
    console.error('Unable to copy to clipboard', err);
  }
  document.body.removeChild(textArea);
}
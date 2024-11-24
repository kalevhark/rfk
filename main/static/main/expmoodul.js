const { createApp, ref } = Vue

createApp({
	delimiters: ['[[', ']]'],
	setup() {
		const showVotmetegevused = ref(true)
		const showRFK = ref(false)
		
		// Funktsioon Liikumine
		// Valdkond 1
		const Select01_01 = ref('0')
		const Select01_02 = ref('0')
		const Select01_03 = ref('0')
		const Select01_M = ref('0')
		const Valdkond01Skoor = ref('0')
		const Valdkond01Raskusaste = ref('')
		const FunktsioonLiikumineRaskusaste = ref('')
		
		// Funktsioon Muu
		// Valdkond 2
		const Select02_01 = ref('0')
		const Select02_02 = ref('0')
		const Select02_03 = ref('0')
		const Select02_M = ref('0')
		const Valdkond02Skoor = ref('0')
		const Valdkond02Raskusaste = ref('')
		
		// Valdkond 4
		const Select04_01 = ref('0')
		const Select04_02 = ref('0')
		const Select04_03 = ref('0')
		const Select04_M = ref('0')
		const Valdkond04Skoor = ref('0')
		const Valdkond04Raskusaste = ref('')
		const FunktsioonMuuRaskusaste = ref('')
		
		// Valdkond 3
		const Select03_01_M = ref('0')
		const Valdkond03_01Skoor = ref('0')
		const Valdkond03_01Raskusaste = ref('')
		const FunktsioonNagemineRaskusaste = ref('')
		const Select03_02_M = ref('0')
		const Valdkond03_02Skoor = ref('0')
		const Valdkond03_02Raskusaste = ref('')
		const FunktsioonKuulmineRaskusaste = ref('')
		const Select03_03_M = ref('0')
		const Valdkond03_03Skoor = ref('0')
		const Valdkond03_03Raskusaste = ref('')
		const FunktsioonKeelKoneRaskusaste = ref('')
		
		// Funktsioon Vaimne
		// Valdkond 5
		const Select05_01 = ref('0')
		const Select05_02 = ref('0')
		const Select05_M = ref('0')
		const Valdkond05Skoor = ref('0')
		const Valdkond05Raskusaste = ref('')
		// Valdkond 6
		const Select06_01 = ref('0')
		const Select06_02 = ref('0')
		const Select06_03 = ref('0')
		const Select06_M = ref('0')
		const Valdkond06Skoor = ref('0')
		const Valdkond06Raskusaste = ref('')
		// Valdkond 7
		const Select07_01 = ref('0')
		const Select07_02 = ref('0')
		const Select07_M = ref('0')
		const Valdkond07Skoor = ref('0')
		const Valdkond07Raskusaste = ref('')
		const FunktsioonVaimneRaskusaste = ref('')
		
		const puudeRaskusaste = ref('')
		
		function roundToTwo(num) {
			return +(Math.round(num + "e+2")  + "e-2");
		}
		
		function calcValdkond01() {
			value = parseInt(Select01_M.value)
			if (showVotmetegevused.value === true) {
				value = (parseInt(Select01_01.value) + parseInt(Select01_02.value) + parseInt(Select01_03.value)) / 3
				if (parseInt(Select01_M.value) >= value) {
					value = (parseInt(Select01_01.value) + parseInt(Select01_02.value) + parseInt(Select01_03.value) + parseInt(Select01_M.value)) / 4
				}
			}
				Valdkond01Skoor.value = roundToTwo(value).toFixed(2)
			
				value = ''
			if (Valdkond01Skoor.value >= 2) {
				value = 'Keskmine'
			}
			if (Valdkond01Skoor.value >= 2.76) {
				value = 'Raske'
			}
			if (Valdkond01Skoor.value >= 3.5) {
				value = 'Sügav'
			}
			Valdkond01Raskusaste.value = value
			calcFunktsioonLiikumine()
			calcPuudeRaskusaste()
		}
		
		function calcFunktsioonLiikumine() {
			value = ''
			if (Valdkond01Skoor.value >= 2) {
				value = 'Keskmine'
			}
			if (Valdkond01Skoor.value >= 2.76) {
				value = 'Raske'
			}
			if (Valdkond01Skoor.value >= 3.5) {
				value = 'Sügav'
			}
			FunktsioonLiikumineRaskusaste.value = value
		}

		function calcValdkond02() {
			value = parseInt(Select02_M.value)
			if (showVotmetegevused.value === true) {
				value = (parseInt(Select02_01.value) + parseInt(Select02_02.value) + parseInt(Select02_03.value)) / 3
				if (parseInt(Select02_M.value) >= value) {
					value = (parseInt(Select02_01.value) + parseInt(Select02_02.value) + parseInt(Select02_03.value) + parseInt(Select02_M.value)) / 4
				}
			}
				Valdkond02Skoor.value = roundToTwo(value).toFixed(2)
			
				value = ''
			if (Valdkond02Skoor.value >= 2) {
				value = 'Keskmine'
			}
			if (Valdkond02Skoor.value >= 2.76) {
				value = 'Raske'
			}
			if (Valdkond02Skoor.value >= 3.5) {
				value = 'Sügav'
			}
			Valdkond02Raskusaste.value = value
			calcFunktsioonMuu()
			calcPuudeRaskusaste()
		}
		
		function calcValdkond04() {
			value = parseInt(Select04_M.value)
			if (showVotmetegevused.value === true) {
				value = (parseInt(Select04_01.value) + parseInt(Select04_02.value) + parseInt(Select04_03.value)) / 3
				if (parseInt(Select04_M.value) >= value) {
					value = (parseInt(Select04_01.value) + parseInt(Select04_02.value) + parseInt(Select04_03.value) + parseInt(Select04_M.value)) / 4
				}
			}
				Valdkond04Skoor.value = roundToTwo(value).toFixed(2)
			
				value = ''
			if (Valdkond04Skoor.value >= 2.76) {
				value = 'Keskmine'
			}
			if (Valdkond04Skoor.value >= 3.5) {
				value = 'Raske'
			}
			Valdkond04Raskusaste.value = value
			calcFunktsioonMuu()
			calcPuudeRaskusaste()
		}
		
		function calcFunktsioonMuu() {
			raskusastmed = ['', 'Keskmine', 'Raske', 'Sügav']
			// Valdkond 2
			value02 = 0
			if (Valdkond02Skoor.value >= 2) {
				value02 = 1
			}
			if (Valdkond02Skoor.value >= 2.76) {
				value02 = 2
			}
			if (Valdkond02Skoor.value >= 3.5) {
				value02 = 3
			}
			// Valdkond 4
			value04 = 0
			if (Valdkond04Skoor.value >= 2.76) {
				value04 = 1
			}
			if (Valdkond04Skoor.value >= 3.5) {
				value04 = 2
			}
			value = Math.max(value02, value04)
			FunktsioonMuuRaskusaste.value = raskusastmed[value]
		}
		
		function calcValdkond03_01() {
				value = parseInt(Select03_01_M.value)
				Valdkond03_01Skoor.value = roundToTwo(value).toFixed(2)
			
				value = ''
			if (Valdkond03_01Skoor.value >= 2) {
				value = 'Keskmine'
			}
			if (Valdkond03_01Skoor.value >= 2.76) {
				value = 'Raske'
			}
			if (Valdkond03_01Skoor.value >= 3.5) {
				value = 'Sügav'
			}
			Valdkond03_01Raskusaste.value = value
			calcFunktsioonNagemine()
			calcPuudeRaskusaste()
		}
		
		function calcFunktsioonNagemine() {
			value = ''
			if (Valdkond03_01Skoor.value >= 2) {
				value = 'Keskmine'
			}
			if (Valdkond03_01Skoor.value >= 2.76) {
				value = 'Raske'
			}
			if (Valdkond03_01Skoor.value >= 3.5) {
				value = 'Sügav'
			}
			FunktsioonNagemineRaskusaste.value = value
		}
		
		function calcValdkond03_02() {
				value = parseInt(Select03_02_M.value)
				Valdkond03_02Skoor.value = roundToTwo(value).toFixed(2)
			
				value = ''
			if (Valdkond03_02Skoor.value >= 2) {
				value = 'Keskmine'
			}
			if (Valdkond03_02Skoor.value >= 2.76) {
				value = 'Raske'
			}
			if (Valdkond03_02Skoor.value >= 3.5) {
				value = 'Sügav'
			}
			Valdkond03_02Raskusaste.value = value
			calcFunktsioonKuulmine()
			calcPuudeRaskusaste()
		}
		
		function calcFunktsioonKuulmine() {
			value = ''
			if (Valdkond03_02Skoor.value >= 2) {
				value = 'Keskmine'
			}
			if (Valdkond03_02Skoor.value >= 2.76) {
				value = 'Raske'
			}
			if (Valdkond03_02Skoor.value >= 3.5) {
				value = 'Sügav'
			}
			FunktsioonKuulmineRaskusaste.value = value
		}
		
		function calcValdkond03_03() {
				value = parseInt(Select03_03_M.value)
				Valdkond03_03Skoor.value = roundToTwo(value).toFixed(2)
			
				value = ''
			if (Valdkond03_03Skoor.value >= 2) {
				value = 'Keskmine'
			}
			if (Valdkond03_03Skoor.value >= 2.76) {
				value = 'Raske'
			}
			if (Valdkond03_03Skoor.value >= 3.5) {
				value = 'Sügav'
			}
			Valdkond03_03Raskusaste.value = value
			calcFunktsioonKeelKone()
			calcPuudeRaskusaste()
		}
		
		function calcFunktsioonKeelKone() {
			value = ''
			if (Valdkond03_03Skoor.value >= 2) {
				value = 'Keskmine'
			}
			if (Valdkond03_03Skoor.value >= 2.76) {
				value = 'Raske'
			}
			if (Valdkond03_03Skoor.value >= 3.5) {
				value = 'Sügav'
			}
			FunktsioonKeelKoneRaskusaste.value = value
		}
		
		function calcValdkond05() {
			value = parseInt(Select05_M.value)
				if (showVotmetegevused.value === true) {
				value = (parseInt(Select05_01.value) + parseInt(Select05_02.value)) / 2
				if (parseInt(Select05_M.value) >= value) {
					value = (parseInt(Select05_01.value) + parseInt(Select05_02.value) + parseInt(Select05_M.value)) / 3
				}
			}
				Valdkond05Skoor.value = roundToTwo(value).toFixed(2)
			
				value = ''
			if (Valdkond05Skoor.value >= 2) {
				value = 'Keskmine'
			}
			if (Valdkond05Skoor.value >= 2.76) {
				value = 'Raske'
			}
			if (Valdkond05Skoor.value >= 3.5) {
				value = 'Sügav'
			}
			Valdkond05Raskusaste.value = value
			calcFunktsioonVaimne()
			calcPuudeRaskusaste()
		}
		
		function calcValdkond06() {
			value = parseInt(Select06_M.value)
			if (showVotmetegevused.value === true) {
				value = (parseInt(Select06_01.value) + parseInt(Select06_02.value) + parseInt(Select06_03.value)) / 3
				if (parseInt(Select06_M.value) >= value) {
					value = (parseInt(Select06_01.value) + parseInt(Select06_02.value) + parseInt(Select06_03.value) + parseInt(Select06_M.value)) / 4
				}
			}
				Valdkond06Skoor.value = roundToTwo(value).toFixed(2)
			
				value = ''
			if (Valdkond06Skoor.value >= 2) {
				value = 'Keskmine'
			}
			if (Valdkond06Skoor.value >= 2.76) {
				value = 'Raske'
			}
			if (Valdkond06Skoor.value >= 3.5) {
				value = 'Sügav'
			}
			Valdkond06Raskusaste.value = value
			calcFunktsioonVaimne()
			calcPuudeRaskusaste()
		}
		
		function calcValdkond07() {
			value = parseInt(Select07_M.value)
			if (showVotmetegevused.value === true) {
				value = (parseInt(Select07_01.value) + parseInt(Select07_02.value)) / 2
				if (parseInt(Select07_M.value) >= value) {
					value = (parseInt(Select07_01.value) + parseInt(Select07_02.value) + parseInt(Select07_M.value)) / 3
				}
			}
				Valdkond07Skoor.value = roundToTwo(value).toFixed(2)
			
				value = ''
			if (Valdkond07Skoor.value >= 2) {
				value = 'Keskmine'
			}
			if (Valdkond07Skoor.value >= 2.76) {
				value = 'Raske'
			}
			if (Valdkond07Skoor.value >= 3.5) {
				value = 'Sügav'
			}
			Valdkond07Raskusaste.value = value
			calcFunktsioonVaimne()
			calcPuudeRaskusaste()
		}
		
		function calcFunktsioonVaimne() {
			raskusastmed = ['', 'Keskmine', 'Raske', 'Sügav']
			// Valdkond 5
			value05 = 0
			if (Valdkond05Skoor.value >= 2) {
				value05 = 1
			}
			if (Valdkond05Skoor.value >= 2.76) {
				value05 = 2
			}
			if (Valdkond05Skoor.value >= 3.5) {
				value05 = 3
			}
			// Valdkond 6
			value06 = 0
			if (Valdkond06Skoor.value >= 2) {
				value06 = 1
			}
			if (Valdkond06Skoor.value >= 2.76) {
				value06 = 2
			}
			if (Valdkond06Skoor.value >= 3.5) {
				value06 = 3
			}
			// Valdkond 7
			value07 = 0
			if (Valdkond07Skoor.value >= 2) {
				value07 = 1
			}
			if (Valdkond07Skoor.value >= 2.76) {
				value07 = 2
			}
			if (Valdkond07Skoor.value >= 3.5) {
				value07 = 3
			}
			value = Math.max(value05, value06, value07)
			FunktsioonVaimneRaskusaste.value = raskusastmed[value]
		}
		
		function calcPuudeRaskusaste() {
			raskusastmed = ['', 'Keskmine puue', 'Raske puue', 'Sügav puue']
			// Valdkond 1
			value01 = 0
			if (Valdkond01Skoor.value >= 2) {
				value01 = 1
			}
			if (Valdkond01Skoor.value >= 2.76) {
				value01 = 2
			}
			if (Valdkond01Skoor.value >= 3.5) {
				value01 = 3
			}
			// Valdkond 2
			value02 = 0
			if (Valdkond02Skoor.value >= 2) {
				value02 = 1
			}
			if (Valdkond02Skoor.value >= 2.76) {
				value02 = 2
			}
			if (Valdkond02Skoor.value >= 3.5) {
				value02 = 3
			}
			// Valdkond 4
			value04 = 0
			if (Valdkond04Skoor.value >= 2.76) {
				value04 = 1
			}
			if (Valdkond04Skoor.value >= 3.5) {
				value04 = 2
			}
			// Valdkond 3_1
			value03_01 = 0
			if (Valdkond03_01Skoor.value >= 2) {
				value03_01 = 1
			}
			if (Valdkond03_01Skoor.value >= 2.76) {
				value03_01 = 2
			}
			if (Valdkond03_01Skoor.value >= 3.5) {
				value03_01 = 3
			}
			// Valdkond 3_2
			value03_02 = 0
			if (Valdkond03_02Skoor.value >= 2) {
				value03_02 = 1
			}
			if (Valdkond03_02Skoor.value >= 2.76) {
				value03_02 = 2
			}
			if (Valdkond03_02Skoor.value >= 3.5) {
				value03_02 = 3
			}
			// Valdkond 3_3
			value03_03 = 0
			if (Valdkond03_03Skoor.value >= 2) {
				value03_03 = 1
			}
			if (Valdkond03_03Skoor.value >= 2.76) {
				value03_03 = 2
			}
			if (Valdkond03_03Skoor.value >= 3.5) {
				value03_03 = 3
			}
			// Valdkond 5
			value05 = 0
			if (Valdkond05Skoor.value >= 2) {
				value05 = 1
			}
			if (Valdkond05Skoor.value >= 2.76) {
				value05 = 2
			}
			if (Valdkond05Skoor.value >= 3.5) {
				value05 = 3
			}
			// Valdkond 6
			value06 = 0
			if (Valdkond06Skoor.value >= 2) {
				value06 = 1
			}
			if (Valdkond06Skoor.value >= 2.76) {
				value06 = 2
			}
			if (Valdkond06Skoor.value >= 3.5) {
				value06 = 3
			}
			// Valdkond 7
			value07 = 0
			if (Valdkond07Skoor.value >= 2) {
				value07 = 1
			}
			if (Valdkond07Skoor.value >= 2.76) {
				value07 = 2
			}
			if (Valdkond07Skoor.value >= 3.5) {
				value07 = 3
			}
			value = Math.max(value01, Math.max(value02, value04), value03_01, value03_02, value03_03, Math.max(value05, value06, value07))
			puudeRaskusaste.value = raskusastmed[value]
		}
		
		return {
			showVotmetegevused,
			showRFK,
			Select01_01,
			Select01_02,
			Select01_03,
			Select01_M,
			Valdkond01Skoor,
			Valdkond01Raskusaste,
			calcValdkond01,
			FunktsioonLiikumineRaskusaste,
			calcFunktsioonLiikumine,
			Select02_01,
			Select02_02,
			Select02_03,
			Select02_M,
			Valdkond02Skoor,
			Valdkond02Raskusaste,
			calcValdkond02,
			Select04_01,
			Select04_02,
			Select04_03,
			Select04_M,
			Valdkond04Skoor,
			Valdkond04Raskusaste,
			calcValdkond04,
			FunktsioonMuuRaskusaste,
			calcFunktsioonMuu,
			Select03_01_M,
			Valdkond03_01Skoor,
			Valdkond03_01Raskusaste,
			calcValdkond03_01,
			FunktsioonNagemineRaskusaste,
			calcFunktsioonNagemine,
			Select03_02_M,
			Valdkond03_02Skoor,
			Valdkond03_02Raskusaste,
			calcValdkond03_02,
			FunktsioonKuulmineRaskusaste,
			calcFunktsioonKuulmine,
			Select03_03_M,
			Valdkond03_03Skoor,
			Valdkond03_03Raskusaste,
			calcValdkond03_03,
			FunktsioonKeelKoneRaskusaste,
			calcFunktsioonKeelKone,
			Select05_01,
			Select05_02,
			Select05_M,
			Valdkond05Skoor,
			Valdkond05Raskusaste,
			calcValdkond05,
			Select06_01,
			Select06_02,
			Select06_03,
			Select06_M,
			Valdkond06Skoor,
			Valdkond06Raskusaste,
			calcValdkond06,
			Select07_01,
			Select07_02,
			Select07_M,
			Valdkond07Skoor,
			Valdkond07Raskusaste,
			calcValdkond07,
			FunktsioonVaimneRaskusaste,
			calcFunktsioonVaimne,
			puudeRaskusaste
		}
	},
	mounted() {
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
	},
	methods: {
		
	}
}).mount('#app')

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
			// checkCodes();
		}
	}
}

// $( document ).ready(function() {})
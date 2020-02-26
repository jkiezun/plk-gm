var availablePlayers = [];
var clubs = getClubsList();
var chosenPlayers = [];
var allPlayers = [];
var capId = NaN;
var benchIds = [];
var sixthManId = NaN;

const selectedClub = document.querySelector("#club-filter");
selectedClub.addEventListener("change", event => {
	updatePlayersList(event.target.value);
});

function updatePlayersList(clubId) {
	var chosenPlayersPks = chosenPlayers.map(e => e.pk);
	availablePlayers = allPlayers;
	availablePlayers = availablePlayers.filter(
		player => !chosenPlayersPks.includes(player.pk)
	);
	if (clubId != "all-teams") {
		availablePlayers = availablePlayers.filter(
			player => player.fields.Club == parseInt(clubId)
		);
	}
	displayAvailablePlayers();
}

function displayAvailablePlayers() {
	var playersTable = document.getElementById("available-players-table");
	var playersList = availablePlayers;

	playersTable.innerHTML = "";

	addAvailablePlayersTableHeaders(playersTable);

	for (let j = 0; j < playersList.length; j++) {
		playersTable.append(createPlusRow(playersList[j]));

		plusButton = document.getElementById("add" + playersList[j].pk); // get the button which is actually in the DOM
		plusButton.addEventListener("click", () => {
			console.log(playersList[j]);
			plusButtonFunctionality(playersList[j]);
		});

		infoButton = document.getElementById("info-add" + playersList[j].pk); // get the button which is actually in the DOM
		infoButton.addEventListener("click", () => {
			infoButtonFunctionality(playersList[j]);
		});
	}
}

function displayChosenPlayers() {
	var playersTable = document.getElementById("chosen-players-table");
	var playersList = chosenPlayers;

	playersTable.innerHTML = "";

	addChosenPlayersTableHeaders(playersTable);
	for (let j = 0; j < playersList.length; j++) {
		playersTable.append(createMinusRow(playersList[j]));

		minusButton = document.getElementById("rm" + playersList[j].pk); // get button which is actually in the DOM
		minusButton.addEventListener("click", () => {
			console.log(playersList[j]);
			minusButtonFunctionality(playersList[j].pk);
		});

		infoButton = document.getElementById("info-rm" + playersList[j].pk); // get the button which is actually in the DOM
		infoButton.addEventListener("click", () => {
			infoButtonFunctionality(playersList[j]);
		});

		let capCheckbox = document.getElementById("cap" + playersList[j].pk);
		let benchCheckbox = document.getElementById("bench" + playersList[j].pk);
		let sixthManCheckbox = document.getElementById(
			"sixthman" + playersList[j].pk
		);

		capCheckbox.addEventListener("change", () => {
			if (capCheckbox.checked) {
				if (isNaN(capId) && sixthManCheckbox.checked == false) {
					capId = playersList[j].pk;
					console.log("cap" + playersList[j].pk);
					console.log(capId);
				} else if (!isNaN(capId)) {
					alert("You can choose only one captain.");
					capCheckbox.checked = false;
				} else {
					alert("One player cannot be both captain and sixth man.");
					capCheckbox.checked = false;
				}
			} else {
				capId = NaN;
				console.log("notcap" + playersList[j].pk);
			}
		});

		benchCheckbox.addEventListener("change", () => {
			if (benchCheckbox.checked) {
				console.log("bench" + playersList[j].pk);
			} else {
				console.log("notbench" + playersList[j].pk);
			}
		});

		sixthManCheckbox.addEventListener("change", () => {
			if (sixthManCheckbox.checked) {
				console.log("sixth" + playersList[j].pk);
			} else {
				console.log("notsixth" + playersList[j].pk);
			}
		});
	}
}

function addAvailablePlayersTableHeaders(playersTable) {
	var tHeader = document.createElement("th");
	tHeader.innerText = "Imię";
	playersTable.append(tHeader);
	var tHeader = document.createElement("th");
	tHeader.innerText = "Nazwisko";
	playersTable.append(tHeader);
	var tHeader = document.createElement("th");
	tHeader.innerText = "Klub";
	playersTable.append(tHeader);
	var tHeader = document.createElement("th");
	tHeader.innerText = "Pozycja";
	playersTable.append(tHeader);
	var tHeader = document.createElement("th");
	tHeader.innerText = "Dodaj";
	playersTable.append(tHeader);
	var tHeader = document.createElement("th");
	tHeader.innerText = "Info";
	playersTable.append(tHeader);
}

function addChosenPlayersTableHeaders(playersTable) {
	var tHeader = document.createElement("th");
	tHeader.innerText = "Imię";
	playersTable.append(tHeader);
	var tHeader = document.createElement("th");
	tHeader.innerText = "Nazwisko";
	playersTable.append(tHeader);
	var tHeader = document.createElement("th");
	tHeader.innerText = "Klub";
	playersTable.append(tHeader);
	var tHeader = document.createElement("th");
	tHeader.innerText = "Pozycja";
	playersTable.append(tHeader);
	var tHeader = document.createElement("th");
	tHeader.innerText = "Kapitan";
	playersTable.append(tHeader);
	var tHeader = document.createElement("th");
	tHeader.innerText = "Ławka";
	playersTable.append(tHeader);
	var tHeader = document.createElement("th");
	tHeader.innerText = "6man";
	playersTable.append(tHeader);
	var tHeader = document.createElement("th");
	tHeader.innerText = "Usuń";
	playersTable.append(tHeader);
	var tHeader = document.createElement("th");
	tHeader.innerText = "Info";
	playersTable.append(tHeader);
}

function createPlusRow(player) {
	var row = document.createElement("tr");
	for (key in player.fields) {
		if (key != "number") {
			var cell = document.createElement("td");
			if (key == "first_name" || key == "last_name") {
				cell.classList += "left-align";
			}
			cell.innerHTML = player.fields[key];
			row.append(cell);
		}
	}
	var plusButton = createButton(
		"plus-button table-button",
		"add" + player.pk,
		"+"
	);
	var infoButton = createButton(
		"info-button table-button",
		"info-add" + player.pk,
		"i"
	);

	let plusButtonCell = document.createElement("td");
	plusButtonCell.innerHTML = plusButton.outerHTML;
	row.append(plusButtonCell); // button get appended and appears in DOM

	let infoButtonCell = document.createElement("td");
	infoButtonCell.innerHTML = infoButton.outerHTML;
	row.append(infoButtonCell);

	return row;
}

function createMinusRow(player) {
	var row = document.createElement("tr");
	for (key in player.fields) {
		if (key != "number") {
			var cell = document.createElement("td");
			if (key == "first_name" || key == "last_name") {
				cell.classList += "left-align";
			}
			cell.innerHTML = player.fields[key];
			row.append(cell);
		}
	}

	var minusButton = createButton(
		"minus-button table-button",
		"rm" + player.pk,
		"-"
	);
	var infoButton = createButton(
		"info-button table-button",
		"info-rm" + player.pk,
		"i"
	);

	let checkboxCell = document.createElement("td");
	let checkbox = createCheckbox("", "cap" + player.pk);
	checkboxCell.innerHTML = checkbox.outerHTML;
	row.append(checkboxCell);

	checkboxCell = document.createElement("td");
	checkbox = createCheckbox("", "bench" + player.pk);
	checkboxCell.innerHTML = checkbox.outerHTML;
	row.append(checkboxCell);

	checkboxCell = document.createElement("td");
	checkbox = createCheckbox("", "sixthman" + player.pk);
	checkboxCell.innerHTML = checkbox.outerHTML;
	row.append(checkboxCell);

	let minusButtonCell = document.createElement("td");
	minusButtonCell.innerHTML = minusButton.outerHTML;
	row.append(minusButtonCell); // button get appended and appears in DOM

	let infoButtonCell = document.createElement("td");
	infoButtonCell.innerHTML = infoButton.outerHTML;
	row.append(infoButtonCell);

	return row;
}

function plusButtonFunctionality(player) {
	chosenPlayersFromClub = chosenPlayers.filter(
		el => el.fields["Club"] == player.fields["Club"]
	);

	if (Object.keys(chosenPlayers).length == 10) {
		alert("You can only choose 10 players");
	} else if (Object.keys(chosenPlayersFromClub).length == 3) {
		alert("You can only choose 3 players from the same club.");
	} else {
		chosenPlayers.push(availablePlayers.find(el => el.pk == player.pk));
		availablePlayers = availablePlayers.filter(el => el.pk != player.pk);
		displayAvailablePlayers();
		displayChosenPlayers();
		console.log(chosenPlayers);
		console.log(availablePlayers);
	}
}

function minusButtonFunctionality(player_id) {
	if (capId == player_id) {
		capId = NaN;
	}
	availablePlayers.push(chosenPlayers.find(player => player.pk == player_id));
	chosenPlayers = chosenPlayers.filter(player => player.pk != player_id);
	updatePlayersList(selectedClub.value); // so that available players are in the same order
	displayChosenPlayers();
	console.log(chosenPlayers);
	console.log(availablePlayers);
}

function infoButtonFunctionality(player) {
	$("#exampleModalCenter .modal-title").html(
		player.fields["first_name"] + " " + player.fields["last_name"]
	);
	$("#exampleModalCenter .modal-body").html(
		"Player " + player.fields["last_name"] + " modal."
	);
	$("#exampleModalCenter").modal("show");
}

function getClubsList() {
	var x = document.getElementById("club-filter");
	var clubs = [];
	for (var i = 1; i < x.options.length; i++) {
		clubs.push(x.options[i].text);
	}
	return clubs;
}

function createButton(btnClasses, btnId, btnText) {
	var tmpButton = document.createElement("button");
	tmpButton.classList += btnClasses;
	tmpButton.id = btnId;
	tmpButton.innerHTML = btnText;
	return tmpButton;
}

function createCheckbox(checkClasses, checkId) {
	let checkbox = document.createElement("input");
	checkbox.setAttribute("type", "checkbox");
	checkbox.id = checkId;
	checkbox.classList += checkClasses;
	return checkbox;
}

$.ajax({
	url: "fantasy/players/",
	dataType: "json",
	type: "GET",
	contentType: "application/json",
	success: function(data) {
		console.log("o");
		data = JSON.parse(data);
		availablePlayers = data;
		allPlayers = data;
		displayAvailablePlayers();
	}
});

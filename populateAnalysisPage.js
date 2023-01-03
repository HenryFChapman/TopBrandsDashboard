
const urlParams = new URLSearchParams(window.location.search);
const myParam = decodeURI(urlParams.get('company').replace("*", "&"));

history.pushState(null, null, myParam);

//Replace Flavor Text With Description
d3.csv("entities.csv").then(function(data) {

	for (var i = 0; i < data.length; i++) {
		if (data[i].EntityName == myParam) {

			document.getElementsByTagName("h2")[0].innerHTML = (i+1).toString() + ". " + myParam;
			document.getElementsByTagName("p")[0].innerHTML = data[i].WikiDescrip;
			document.getElementsByTagName("h4")[0].innerHTML = "Infegy Trust Score: " + data[i].trustMetric + "<br>Post Volume: " + data[i].totalDocuments

			var tempCard = document.getElementsByClassName("analysisCard")[0];

			var img = document.createElement("img");
			img.src = "assets/logos/" + data[i].EntityName + ".png";
			img.alt = "Image";

			picture = document.createElement("picture");
			picture.className = "thumbnail";
			picture.appendChild(img);

			tempCard.appendChild(picture);
		}

	}
}).catch(function(error) {
	console.log(error);
});;

d3.csv("data/volume/"+myParam+".csv").then(function(data) {

	var dates = new Array(data.length);
	var volumes = new Array(data.length);

	for (var i = 0; i< data.length; i++) {

		dates[i] = data[i].Date.split('T')[0];
		volumes[i] = data[i].Universe;
	}

	//This Section Does Post Volume Graph
	var data1 = {
		labels: dates,
		datasets: [{
			label: "Post Volume",
			backgroundColor: "#846FC6",
			borderColor: "#846FC6",
			borderWidth: 2,
			data: volumes,
		}]
	};

	var options1 = {
		maintainAspectRatio: false,
		responsive: true,
		scales: {
			yAxes: [{
				stacked: true,
				gridLines: {
					display: false,
					color: "#000000"
				},
				scaleLabel: {
					display: true,
					labelString: 'Post Volume'
				}
			}],
			xAxes: [{
				gridLines: {
					display: false,
					color: "#000000"
				},
			}]
		}
	};

	var graph = new Chart('chart-1', {
		type: 'line',
		options: options1,
		data: data1
	});
}).catch(function(error) {
	console.log(error);
});

d3.csv("data/sentiment/"+myParam+".csv").then(function(data) {

	posColour = "#75C0B37A"
	negColour = 'rgba(255, 0, 0, .1)'

	var dates = new Array(data.length);
	var volumes = new Array(data.length);

	for (var i = 0; i< data.length; i++) {

		dates[i] = data[i].Date.split('T')[0];
		volumes[i] = data[i]['Net Sentiment'];
	}

	//This Section Does Post Volume Graph
	var data1 = {
		labels: dates,
		datasets: [{
			label: "Sentiment",
			backgroundColor: "#2D4F7C",
			borderColor: "#2D4F7C",
			borderWidth: 2,
			data: volumes,
			fill: {
				target: 'origin',
				above: posColour,
				below: negColour
			}
		}]
	};

	var options1 = {
		maintainAspectRatio: false,
		responsive: true,
		scales: {
			yAxes: [{
				stacked: true,
				gridLines: {
					display: false,
					color: "#000000"
				},
				scaleLabel: {
					display: true,
					labelString: 'Post Volume'
				}
			}],
			xAxes: [{
				gridLines: {
					display: false,
					color: "#000000"
				},
			}]
		}
	};

	var graph = new Chart('chart-2', {
		type: 'line',
		options: options1,
		data: data1, 
	});
}).catch(function(error) {
	console.log(error);
});

d3.csv("data/topics/"+myParam+".csv").then(function(data) {

	var myWords = new Array(data.Topic);
	var posRate = new Array(data.Topic);
	var colors = new Array(data.Topic);


	for (var i = 0; i< data.length; i++) {

		myWords[i] = data[i].Topic;
		posRate[i] = data[i]['documents'];
		colors[i] = data[i]['colors'];

		console.log(data[i]['positive_percentage'])

	}

	//This Section Does Post Volume Graph
	var data1 = {
		labels: myWords,
		datasets: [{
			label: "Number of Documents Containing Topic",
			backgroundColor: colors,
			borderColor: colors,
			borderWidth: 2,
			data: posRate,
		}]
	};

	var graph = new Chart('chart-3', {
		type: 'bar',
		data: data1, 
	});

}).catch(function(error) {
	console.log(error);
});


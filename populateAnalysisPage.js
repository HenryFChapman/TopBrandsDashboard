
const urlParams = new URLSearchParams(window.location.search);
const myParam = urlParams.get('company');

console.log(myParam);


//Replace Flavor Text With Description
d3.csv("entities.csv").then(function(data) {

	for (var i = 0; i < data.length; i++) {
		if (data[i].EntityName == myParam) {

			document.getElementsByTagName("h2")[0].innerHTML = myParam;
			document.getElementsByTagName("p")[0].innerHTML = data[i].WikiDescrip;
			document.getElementsByTagName("h4")[0].innerHTML = "Infegy Trust Metric: " + data[i].trustMetric; 

			var tempCard = document.getElementsByClassName("analysisCard")[0];

			console.log(tempCard);

			var img = document.createElement("img");
			img.src = "assets/logos/" + data[i].EntityName + ".png";
			img.alt = "A banana that looks like a bird";

			picture = document.createElement("picture");
			picture.className = "thumbnail";
			picture.appendChild(img);

			tempCard.appendChild(picture);
			console.log("test");

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
			backgroundColor: "#75C0B37A",
			borderColor: "#75C0B3",
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

	var graph = Chart.Line('chart-1', {
		options: options1,
		data: data1
	});
}).catch(function(error) {
	console.log(error);
});

d3.csv("data/sentiment/"+myParam+".csv").then(function(data) {

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
			backgroundColor: "#75C0B37A",
			borderColor: "#75C0B3",
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
					labelString: 'Net Sentiment'
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

	var graph = Chart.Line('chart-2', {
		options: options1,
		data: data1
	});
}).catch(function(error) {
	console.log(error);
});





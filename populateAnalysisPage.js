
const urlParams = new URLSearchParams(window.location.search);
const myParam = decodeURI(urlParams.get('company').replace("*", "&"));

//history.pushState(null, null, myParam);

//Replace Flavor Text With Description
d3.csv("entities.csv").then(function(data) {

	for (var i = 0; i < data.length; i++) {
		if (data[i].EntityName == myParam) {

			document.getElementsByTagName("h2")[0].innerHTML = (i+1).toString() + ". " + myParam;
			document.getElementsByTagName("p")[0].innerHTML = data[i].WikiDescrip;
			document.getElementsByTagName("h4")[0].innerHTML = "Infegy Trust Score: " + data[i].trustMetric + "<br>Post Volume: " + data[i].totalDocuments


			document.getElementsByTagName("h2")[1].innerHTML = myParam + " Post Volume";
			document.getElementsByTagName("h2")[2].innerHTML = myParam + " Net Sentiment";
			document.getElementsByTagName("h2")[3].innerHTML = myParam + " Top Topics";
			document.getElementsByTagName("h2")[4].innerHTML = myParam + " Narratives";


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
		plugins: {
			legend: {
				display: false
			},
		},
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
		plugins: {
			legend: {
				display: false
			},
		},
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


	for (var i = 0; i< 10; i++) {

		myWords[i] = data[i].Topic;
		posRate[i] = data[i]['documents'];
		colors[i] = data[i]['colors'];
	}

	//This Section Does Post Volume Graph
	var data1 = {
		labels: myWords,
		datasets: [{
			label: "Number of Documents Containing Topic",
			backgroundColor: colors,
			borderWidth: 2,
			data: posRate,
		}]
	};

	var options1 = {
		maintainAspectRatio: false,
		responsive: true,
		plugins: {
			legend: {
				display: false
			},
		},
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

	var graph = new Chart('chart-3', {
		type: 'bar',
		data: data1,
		options: options1,
	});

}).catch(function(error) {
	console.log(error);
});


fetch("data/networks/"+myParam+".json").then(res => res.json()).then(data => {

	addEventListener("resize", (event) => {
		const heightOutput = window.innerHeight;

		const widthOutput = window.innerWidth;

		const graph = ForceGraph()
		(document.getElementById('chart-4'))
		.graphData(data)
		.nodeId('id')
		.nodeVal('val')
		.nodeLabel('name')
		.nodeAutoColorBy('cluster_id')
		.linkSource('source')
		.linkTarget('target')
		.enableZoomPanInteraction(false)
		.width(widthOutput)
		.height(heightOutput*.70)
		.nodeCanvasObjectMode(() => "after")
		.nodeCanvasObject((node, ctx, globalScale) => {

			if (node.mainLabel != "No") {
				label = node.name;

				const fontSize = 15 / globalScale;
				ctx.font = `${fontSize}px Sans-Serif`;
				ctx.textAlign = "center";
				ctx.textBaseline = "middle";
				ctx.fillStyle = "#2d333a";
				ctx.fillText(label, node.x, node.y + 20);
			}

		})

		graph.d3Force('charge', d3.forceManyBody().strength(-60));
		graph.d3Force('gravity-x', d3.forceX(window.innerWidth / 2).strength(0.1));
		graph.d3Force('gravity-y', d3.forceY(window.innerHeight / 2).strength(0.1));
		graph.d3Force('collide', d3.forceCollide(graph.nodeRelSize()));
		graph.linkColor(() => "#D3D3D3");

	});

	const graph = ForceGraph()
	(document.getElementById('chart-4'))
	.graphData(data)
	.nodeId('id')
	.nodeVal('val')
	.nodeLabel('name')
	.nodeAutoColorBy('cluster_id')
	.linkSource('source')
	.linkTarget('target')
	.enableZoomPanInteraction(false)
	.height(window.innerHeight*.70)
	.nodeCanvasObjectMode(() => "after")
	.nodeCanvasObject((node, ctx, globalScale) => {

		if (node.mainLabel != "No") {
			label = node.name;

			const fontSize = 15 / globalScale;
			ctx.font = `${fontSize}px Sans-Serif`;
			ctx.textAlign = "center";
			ctx.textBaseline = "middle";
			ctx.fillStyle = "#2d333a";
			ctx.fillText(label, node.x, node.y + 20);
		}

	})

	graph.d3Force('charge', d3.forceManyBody().strength(-60));
	graph.d3Force('gravity-x', d3.forceX(window.innerWidth / 2).strength(0.1));
	graph.d3Force('gravity-y', d3.forceY(window.innerHeight / 2).strength(0.1));
	graph.d3Force('collide', d3.forceCollide(graph.nodeRelSize()));

	graph.linkColor(() => "#D3D3D3");
});





const urlParams = new URLSearchParams(window.location.search);
const myParam = decodeURI(urlParams.get('company').replace("*", "&"));

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

		dates[i] = data[i].Date;
		volumes[i] = data[i].Universe;
	}



	"#846FC6"
	//This Section Does Post Volume Graph
	var data1 = {
		labels: dates,
		datasets: [{
			label: "Sentiment",
			backgroundColor: "white",
			borderColor: "#846FC6",
			pointStyle: 'circle',
			borderWidth: 2,
			data: volumes,
			lineTension: 0.3,
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
		responsive: true,
		scales: {
			x: {
				grid: {
					drawOnChartArea:false,
					tickMarkLength: 0, 
				},
				ticks: {
					maxRotation: 0,
					minRotation: 0,
					autoSkip : true,
					color: "darkgrey",

					//callback: function(label, index, labels){
					//	if (label == 0){
					//		return "January 1st, 2022"
					//	} else if (label == 11) {
					//		return "December 1st, 2022"
					//	} else {
					//		return ""
					//	}
					//}
				},
			},
			y: {
				grid: {
					drawOnChartArea:false
				},
				ticks: {
					maxTicksLimit: 4,
					maxRotation: 0,
					minRotation: 0,
					color: "darkgrey",
				},
				title: {
					display: true,
					text: 'Number of Posts',
					color: "darkgrey"
				}
			}
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

	posColour = "#CBE09D"
	negColour = '#E5BFB9'

	var dates = new Array(data.length);
	var volumes = new Array(data.length);

	for (var i = 0; i< data.length; i++) {

		dates[i] = data[i].Date;
		volumes[i] = data[i]['Net Sentiment'];
	}

	//This Section Does Post Volume Graph
	var data1 = {
		labels: dates,
		datasets: [{
			label: "Sentiment",
			backgroundColor: "white",
			borderColor(context) {
				const index = context.dataIndex
				const value = context.dataset.data[index]
				return value < 0 ? '#DFC0BA' : '#CFDFA4'
			},
			pointStyle: 'circle',
			data: volumes,
			lineTension: 0.3,
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
		responsive: true,
		scales: {
			x: {
				grid: {
					drawOnChartArea:false,
					tickMarkLength: 0, 
				},
				ticks: {
					maxRotation: 0,
					minRotation: 0,
					autoSkip : true,
					color: "darkgrey",

					//callback: function(label, index, labels){
					//	if (label == 0){
					//		return "January 1st, 2022"
					//	} else if (label == 11) {
					//		return "December 1st, 2022"
					//	} else {
					//		return ""
					//	}
					//}
				},
			},
			y: {
				grid: {
					drawOnChartArea:false
				},
				ticks: {
					maxTicksLimit: 4,
					maxRotation: 0,
					minRotation: 0,
					color: "darkgrey",
				},
				suggestedMin: -1,
				suggestedMax: 1,
				title: {
					display: true,
					text: 'Net Sentiment',
					color: "darkgrey"
				}
			}
		}
	};

	const threshold = 0;

	var graph = new Chart('chart-2', {
		type: 'line',
		plugins: [{
			afterLayout: chart => {
				let ctx = chart.ctx;
				ctx.save();
				let yAxis = chart.scales.y;
				let yThreshold = yAxis.getPixelForValue(threshold);
				let gradient = ctx.createLinearGradient(0, yAxis.top, 0, yAxis.bottom);
				gradient.addColorStop(0, '#8FC23D');
				let offset = 1 / yAxis.bottom * yThreshold;
				gradient.addColorStop(offset, '#8FC23D');
				gradient.addColorStop(offset, '#DB314E');
				gradient.addColorStop(1, '#DB314E');
				chart.data.datasets[0].borderColor = gradient;
				ctx.restore();
			}
		}],
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
		responsive: true,
		scales: {
			x: {
				grid: {
					drawOnChartArea:false
				},
				ticks: {
					color: "darkgrey"
				}
			},
			y: {
				grid: {
					drawOnChartArea:false
				},
				ticks: {
					maxTicksLimit: 4,
					maxRotation: 0,
					minRotation: 0,
					color: "darkgrey"
				},
				title: {
					display: true,
					text: 'Number of Posts',
					color: "darkgrey"
				}
			}
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




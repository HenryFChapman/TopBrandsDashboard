
dataForAnalysis = {};

window.onpopstate=function()
{

	window.location.replace('https://www.infegy.com/infegys-top-trusted-brands');

}


function makeTopicGraph(topics) {

	var myWords = topics['Topic'];
	var posRate = topics['documents'];
	var colors = topics['colors'];

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
}

function makeSentimentGraph(sentiment) {
	posColour = "#CBE09D"
	negColour = '#E5BFB9'

	var dates = sentiment['Date'];
	var volumes = sentiment['Net Sentiment'];

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
					format: {
						style: 'percent'
					}
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

}

function makePostVolumeGraph(volume) {
	var dates = volume['Date'];
	var volumes = volume['Universe'];

	"#846FC6"
	//This Section Does Post Volume Graph
	var data1 = {
		labels: dates,
		datasets: [{
			label: "Post Volume",
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
}


function clickHandler(brandName) {

	window.scrollTo(0, 0)

	window.history.pushState(null, null, "https://www.infegy.com/infegys-top-trusted-brands/" + brandName);

	//Remove Old Cards
	document.getElementsByClassName("cards")[0].remove();

	//Add New Cards
	var container = document.getElementsByClassName("centered")[1]
	
	//Create Section
	var section = document.createElement("section");
	section.className = "analysisContainer"
	container.appendChild(section);

	container = document.getElementsByClassName("analysisContainer")[0];

	//Add Cards to Analysis Container
	//Info Card
	var infoCard = document.createElement("article");
	infoCard.className = "analysisCard";

	var cardContent = document.createElement("div");
	cardContent.className = 'card-content';

	var H2 = document.createElement("H2")
	H2.innerHTML = brandName;

	var P = document.createElement("p")
	P.innerHTML = dataForAnalysis['entityHashMap'][brandName]['WikiDescrip'];

	var H4 = document.createElement("H4")
	H4.innerHTML = "Infegy Trust Score: " + dataForAnalysis['entityHashMap'][brandName]['trustMetric'] +  "<br> Post Volume: " + dataForAnalysis['entityHashMap'][brandName]['totalDocuments']

	var img = document.createElement("img");
	img.src = "https://www.infegy.com/hubfs/Most%20Trusted%20Brands%202023/logos/" + brandName.replace("'", "") + ".png";
	img.alt = "Image";

	picture = document.createElement("picture");
	picture.className = "thumbnail";
	picture.appendChild(img);

	cardContent.appendChild(picture);
	cardContent.appendChild(H2);
	cardContent.appendChild(P);
	cardContent.appendChild(H4);

	infoCard.append(cardContent);
	container.appendChild(infoCard);


//This section of code makes the post volume chart!
	var postVolumeCard = document.createElement("article");
	postVolumeCard.className = "analysisCard";
	var cardContent = document.createElement("div");
	cardContent.className = 'card-content';
	var H2 = document.createElement("H2");
	H2.innerHTML = brandName + " Post Volume";
	var P = document.createElement("p");
	P.innerHTML = "Post volume shows how many social media users talked about this particular brand throughout the year.";
	var chartContainer = document.createElement("div");
	chartContainer.className = 'chart-container-1'
	var canvas = document.createElement("canvas");
	canvas.id = "chart-1";

	chartContainer.append(canvas);
	cardContent.appendChild(H2);
	cardContent.appendChild(P);
	cardContent.appendChild(chartContainer);
	postVolumeCard.append(cardContent);
	container.appendChild(postVolumeCard)

//This section of code makes the sentiment chart!
	var sentimentChart = document.createElement("article");
	sentimentChart.className = "analysisCard";
	cardContent = document.createElement("div");
	cardContent.className = "card-content";
	H2 = document.createElement("H2");
	H2.innerHTML = brandName + " Net Sentiment";
	P = document.createElement("p");
	P.innerHTML = "Net sentiment shows how brand sentiment changed over time throughout the year. As positive events occured, the brand will show a higher percentage of brand sentiment, while when negative events occured, that sentiment average will drop.";
	chartContainer = document.createElement("div");
	chartContainer.className = 'chart-container-1'
	canvas = document.createElement("canvas");
	canvas.id = "chart-2";

	chartContainer.append(canvas);
	cardContent.appendChild(H2);
	cardContent.appendChild(P);
	cardContent.appendChild(chartContainer);
	sentimentChart.append(cardContent);
	container.appendChild(sentimentChart)

	//This section of code makes the topics bar chart!
	var topicChart = document.createElement("article");
	topicChart.className = "analysisCard";
	cardContent = document.createElement("div");
	cardContent.className = "card-content";
	H2 = document.createElement("H2");
	H2.innerHTML = brandName + " Top Topics";
	P = document.createElement("p");
	P.innerHTML = "This shows frequently occuring phrases social media users mention when talking about a particular brand. Topics are colorized by sentiment with darker greens being more positive, and lighter greens being less positive.";
	chartContainer = document.createElement("div");
	chartContainer.className = 'chart-container-1'
	canvas = document.createElement("canvas");
	canvas.id = "chart-3";

	chartContainer.append(canvas);
	cardContent.appendChild(H2);
	cardContent.appendChild(P);
	cardContent.appendChild(chartContainer);
	topicChart.append(cardContent);
	container.appendChild(topicChart)

	makePostVolumeGraph(dataForAnalysis['volume'][brandName]);
	makeSentimentGraph(dataForAnalysis['sentiment'][brandName])
	makeTopicGraph(dataForAnalysis['topics'][brandName])

}

function populateMainCards() {

	window.location.pathname.split("/").pop()


	d3.json("https://www.infegy.com/hubfs/Most%20Trusted%20Brands%202023/siteData.json").then(function(data) {

		dataForAnalysis = data;

		var entities = data.entities;

   //data is an array of objects, with one object for each row in the CSV file
		for (var i = 0; i < entities.length; i++) {

			var container = document.getElementsByClassName("cards");

    // Create some HTML elements for the cards
			var tempCard = document.createElement("article");
			tempCard.className = "card";

			a = document.createElement("a");
			tempCard.setAttribute("onclick",'clickHandler("'+entities[i].EntityName+'")');

			picture = document.createElement("picture");
			picture.className = "thumbnail";

			var img = document.createElement("img");
			img.src = "https://www.infegy.com/hubfs/Most%20Trusted%20Brands%202023/logos/" + entities[i].EntityName.replace("'", "") + ".png";
			img.alt = entities[i].EntityName + ".png";
			picture.appendChild(img);
			a.appendChild(picture);

			var div = document.createElement("div");
			div.className = "card-content";

			var h2 = document.createElement("H2");
			h2.innerHTML = (i+1).toString() + ". " + entities[i].EntityName;

			var h4 = document.createElement("H4");
			h4.innerHTML = "Infegy Trust Score: " + entities[i].trustMetric + "<br>Post Volume: " + entities[i].totalDocuments

			var p = document.createElement("P");
			p.innerHTML = entities[i].oneSentence;

			div.appendChild(h2);
			div.appendChild(h4);
			div.append(p);
			a.appendChild(div);

			tempCard.appendChild(a);
			container[0].appendChild(tempCard);
		}
	})
	.catch(function(error) {
		console.log(error);
	});
}

function returnToPage() {

	window.history.pushState(null, null, "https://www.infegy.com/infegys-top-trusted-brands");

	//Remove Old Cards
	document.getElementsByClassName("analysisContainer")[0].remove();

	//Add New Cards
	var container = document.getElementsByClassName("centered")[1]
	
	//Create Section
	var section = document.createElement("section");
	section.className = "cards"
	container.appendChild(section);

	populateMainCards();

}

populateMainCards();


d3.csv("entities.csv").then(function(data) {
    //data is an array of objects, with one object for each row in the CSV file
	
    for (var i = 0; i < data.length; i++) {

    	var container = document.getElementsByClassName("cards");

    	// Create some HTML elements for the cards
		var tempCard = document.createElement("article");
		tempCard.className = "card";

		a = document.createElement("a");
		a.href = "analysisPage.html?company=" + encodeURI(data[i].EntityName.replace("&", "*"));

		picture = document.createElement("picture");
		picture.className = "thumbnail";

		var img = document.createElement("img");
		img.src = "assets/logos/" + data[i].EntityName + ".png";
		img.alt = "A banana that looks like a bird";
		picture.appendChild(img);
		a.appendChild(picture);


		var div = document.createElement("div");
		div.className = "card-content";

		var h2 = document.createElement("H2");
		h2.innerHTML = (i+1).toString() + ". " + data[i].EntityName;


		var h4 = document.createElement("H4");
		h4.innerHTML = "Infegy Trust Score: " + data[i].trustMetric + "<br>Post Volume: " + data[i].totalDocuments

		var p = document.createElement("P");
		p.innerHTML = data[i].oneSentence;

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

// Function to display top 10 beers
function buildRecommender(beerstyle){
    
    d3.json(`/recommender/${beerstyle}`).then(data => data.forEach(e => {
        console.log(data)
        let cardBody = d3.select("#top10")
            .append("div")
            .classed("card", true)
            .append("div")
            .classed("card-body", true)
        cardBody.append("h4")
            .classed("card-title", true)
            .text(e.beer_name)
        cardBody.append("h6")
            .classed("card-subtitle mb-2 text-muted", true)
            .text(`Brewery: ${e.brewery_name}`)
        cardBody.append("p")
            .classed("city", true)
            .text(`City: ${e.city}`)
        cardBody.append("p")
            .classed("state", true)
            .text(`State: ${e.state}`)
        cardBody.append("p")
            .classed("country", true)
            .text(`Country: ${e.country}`)
        cardBody.append("p")
            .classed("abv", true)
            .text(`ABV: ${e.abv}`);
        cardBody.append("p")
            .classed("availability", true)
            .text(`Availability: ${e.availability}`);
        }))
    };

// Function to display worst 10 beers
function buildRecommender(beerstyle){
    
    d3.json(`/recommender/${beerstyle}`).then(data => data.forEach(e => {
        console.log(data)
        let cardBody = d3.select("#worst10")
            .append("div")
            .classed("card", true)
            .append("div")
            .classed("card-body", true)
        cardBody.append("h4")
            .classed("card-title", true)
            .text(e.beer_name)
        cardBody.append("h6")
            .classed("card-subtitle mb-2 text-muted", true)
            .text(`Brewery: ${e.brewery_name}`)
        cardBody.append("p")
            .classed("city", true)
            .text(`City: ${e.city}`)
        cardBody.append("p")
            .classed("state", true)
            .text(`State: ${e.state}`)
        cardBody.append("p")
            .classed("country", true)
            .text(`Country: ${e.country}`)
        cardBody.append("p")
            .classed("abv", true)
            .text(`ABV: ${e.abv}`);
        cardBody.append("p")
            .classed("availability", true)
            .text(`Availability: ${e.availability}`);
        }))
    };

//-----------------FUNCTION INITIATOR-----------------//
function init() {

    const firstStyle = dropdown2Names[1];

    drawGaugeABV(firstStyle);
    drawGaugeIBU(firstStyle);
    drawGaugeSRM(firstStyle);
    buildCharts(firstStyle);
    buildRecommender(firstStyle);
    buildImage(firstStyle);

}

//--------create event listeners--------//
function optionChangedOne(newCategory) {
category = newCategory;
d3.select('#selDatasetTwo').html("");
var selectorTwo = d3.select('#selDatasetTwo');
d3.json(`/beerstyle_filtered/${category}`).then((dropdown2Names) =>{
dropdown2Names.forEach((beerstyle) =>{
    selectorTwo
    .append("option")
    .text(beerstyle.Style)
    .property("value", beerstyle.Style);
});
})
}

function optionChangedTwo(newBeerstyle) {
beerstyle = newBeerstyle;
console.log(beerstyle);
d3.select('#description').html(""),
buildCharts(beerstyle);
d3.select('#beerimage').html(""),
buildImage(beerstyle);
d3.select('#top5').html(""),
buildRecommender(beerstyle);

drawGaugeABV(beerstyle);
drawGaugeIBU(beerstyle);
drawGaugeSRM(beerstyle);


                    
}

// call init function  
init();
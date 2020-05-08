//----------------KNN RECOMMENDER JS SCRIPT-----------------//

// Function to display top 10 beer recommenders using KNN model
function buildKNNRecommender(beer_name){

    // Initialize counter to 0
    var count = 0;
    
    d3.json(`/neighbors/${beer_name}`).then(data => data.forEach(e => {

        console.log(data)

        // Add first 5 beers in the first card-deck row under the id = top5neighbors
        if(count<5){
            let cardBody = d3.select("#top5neighbors")
                .append("div")
                .classed("card", true)
                .append("div")
                .classed("card-body", true)
            cardBody.append("h3")
                .classed("card-title", true)
                .text(e.name)
            cardBody.append("h6")
                .classed("card-subtitle mb-2 text-muted", true)
                .text(`Beer Style: ${e.style}`)
            cardBody.append("p")
                .classed("card-text", true)
                .text(`BeerAdvocate Score: ${e.score_mean}`)
            }
        // Add next 5 beers in the second card-deck row under the id = next5neighbors
        else if (count>=5){
            cardBody = d3.select("#next5neighbors")
                .append("div")
                .classed("card", true)
                .append("div")
                .classed("card-body", true)
            cardBody.append("h3")
                .classed("card-title", true)
                .text(e.name)
            cardBody.append("h6")
                .classed("card-subtitle mb-2 text-muted", true)
                .text(`Beer Style: ${e.style}`)
            cardBody.append("p")
                .classed("card-text", true)
                .text(`BeerAdvocate Score: ${e.score_mean}`)
        }
        // increment the counter
        count++;
    }))
};


//-----------------FUNCTION INITIATOR-----------------//
function init() {
    d3.select('#top5neighbors').html(""), 
    d3.select('#next5neighbors').html(""),   
    buildKNNRecommender(beer_name);


}

//-------- Create Event Listener--------//
function optionChangedFour(newBeer) {
    beer_name = newBeer;
    console.log(beer_name)

    d3.select('#top5neighbors').html(""),
    d3.select('#next5neighbors').html(""),
    buildKNNRecommender(beer_name);

}

// call init function 
init();
// Grab the button - dropdown
const dropdown = d3.select("dropdown")

// Add a H2 element
const header = d3.select('#top10').append("h2")

// Placing the table here (outside of a function), ensures that regardless of the number of times the button is selected, only one table appears
const table = d3.select('#top10').append("table")

// Function to predict user preferences
function predictRatings(username){
  
  console.log('hello 2020');

  d3.json(`/userpredict/${username}`).then(data => {
    console.log(data)

    header.text("We're confident you'll enjoy the following beers.")
    
    // let selUser = dropdown.property("value")

    // Wipes the prior table and fills the table with the desired filters
    table.html("")
    const headerRow = table.append("thead").append("tr")
    headerRow.append("th").text("Score")
    headerRow.append("th").text("Name")
    headerRow.append("th").text("Style")
    headerRow.append("th").text("Brewery")

    const tbody = table.append("tbody")

    data.forEach(dataRow => {
      let row = tbody.append("tr")
      row.append("td").text(dataRow.score)
      row.append("td").text(dataRow.name)
      row.append("td").text(dataRow.style)
      row.append("td").text(dataRow.brewery_name)
    })
  })
};

// For testing/demo purposes
predictRatings('michellebrucato')

// NEEDS WORK After the user selects their username, the handler function will execute
// dropdown.on("change", predictRatings);
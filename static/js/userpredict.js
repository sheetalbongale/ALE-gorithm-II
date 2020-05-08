// Grab the button - dropdown
const dropdown = d3.selectAll(".dropdown-menu a")

// Add a H2 element
const topHeader = d3.select('#top10').append("h2")
// Placing the table here (outside of a function), ensures that regardless of the number of times the button is selected, only one table appears
const topTable = d3.select('#top10').append("table")

// Repeat 5 and 7 to create Header and Table for Bottom 10
const botHeader = d3.select('#top10').append("h2")
const botTable = d3.select('#top10').append("table")

// Function to predict user preferences
function predictRatings(){
  // Grab the selected text from dropdown (via event handler)
  let username = d3.select(this).text()
  
  console.log('hello 2020');

  // Pull the data for the corresponding user
  d3.json(`/userpredict/${username}`).then(data => {
    console.log(data)

    topHeader.text("We're confident you'll enjoy the following beers.")
    botHeader.text("Steer clear of these beers, you'll thank us later.")

    // Wipes the prior table and fills the table with the desired filters
    topTable.html("")
    botTable.html("")
    let headerRow = topTable.append("thead").append("tr")
    headerRow.append("th").text("Username")
    headerRow.append("th").text("Prediction")
    headerRow.append("th").text("BAScore")
    headerRow.append("th").text("Name")
    headerRow.append("th").text("Style")
    headerRow.append("th").text("Brewery")

    const topTbody = topTable.append("tbody")

    headerRow = botTable.append("thead").append("tr")
    headerRow.append("th").text("Username")
    headerRow.append("th").text("Prediction")
    headerRow.append("th").text("BAScore")
    headerRow.append("th").text("Name")
    headerRow.append("th").text("Style")
    headerRow.append("th").text("Brewery")

    const botTbody = botTable.append("tbody")

    data.forEach(dataRow => {
      if (dataRow.pick === 'Top10') {
        let row = topTbody.append("tr")
        row.append("td").text(dataRow.username)
        row.append("td").text(dataRow.prediction)
        row.append("td").text(dataRow.score)
        row.append("td").text(dataRow.name)
        row.append("td").text(dataRow.style)
        row.append("td").text(dataRow.brewery_name)
      } else {
        let row = botTbody.append("tr")
        row.append("td").text(dataRow.username)
        row.append("td").text(dataRow.prediction)
        row.append("td").text(dataRow.score)
        row.append("td").text(dataRow.name)
        row.append("td").text(dataRow.style)
        row.append("td").text(dataRow.brewery_name)
      }
    })
  })
};

// After the user selects their username, the handler function will execute
dropdown.on("click", predictRatings);
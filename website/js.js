let meta_data;

const dateInput = document.getElementById("datepicker");
const mapFrame = document.getElementById("map");
const date = document.getElementById("date");
const title = document.getElementById("title");
const source = document.getElementById("source");
const location_name = document.getElementById("location");
const mentioned = document.getElementById("mentioned");
const mentioned_total = document.getElementById("mentioned_total");
const context = document.getElementById("context");
const description = document.getElementById("description");

fetch("meta_data.json")
    .then(response => {
        if (!response.ok) {
            throw new Error("couldn't get json file");
        }
        return response.json();
    })
    .then(data => {
        meta_data = data;
        updateUI(dateInput.value);
    })
    .catch(error => {
        console.error("error fetching json file:", error);
    });

dateInput.addEventListener("change", function() {
    updateUI(this.value);
});

function updateUI(selectedDate) {
    mapFrame.src = "maps/" + selectedDate + ".html";
    date.innerHTML = selectedDate;
    title.innerHTML = "<b>Title: </b>" + meta_data[selectedDate]["title"];
    source.innerHTML = "<b>Source: </b>" + "<a target='_blank' rel='noopener noreferrer' href='" + meta_data[selectedDate]["source"] + "'>" + meta_data[selectedDate]["source"] + "</a>";
    location_name.innerHTML = "";
    mentioned.innerHTML = "";
    mentioned_total.innerHTML = "";
    context.innerHTML = "";
    description.innerHTML = "";
    mapFrame.onload = () => {
        get_click(selectedDate);
    };

}

function get_click(date) {
    const plotWindow = mapFrame.contentWindow;

    const interval = setInterval(() => {
        const plot = plotWindow.document.getElementById(date);
        if (plot && plotWindow.Plotly && typeof plot.on === "function") {
            clearInterval(interval);

            plot.on("plotly_click", function(data) {
                console.log(data.points[0])
                if (data.points[0]["data"]["type"] == "scattermap") {
                    const location_data = data.points[0]["data"]["customdata"];
                    console.log(location_data)
                    location_name.innerHTML = location_data[0];
                    mentioned.innerHTML = "<b>Mentioned this day: </b>" + location_data[1];
                    mentioned_total.innerHTML = "<b>Mentioned total: </b>" + location_data[2];
                    context.innerHTML = "<b>Context: </b>" + location_data[3];
                    description.innerHTML = "<b>Description: </b>" + location_data[4];
                } else {
                    const index = data.points[0]["pointIndex"];
                    const location_data = data.points[0]["data"]["customdata"][index][0];
                    console.log(location_data)
                    location_name.innerHTML = location_data[0];
                    mentioned.innerHTML = "<b>Mentioned this day: </b>" + location_data[1];
                    mentioned_total.innerHTML = "<b>Mentioned total: </b>" + location_data[2];
                    context.innerHTML = "<b>Context: </b>" + location_data[3];
                    description.innerHTML = "<b>Description: </b>" + location_data[4];
                }
            });
        }
    }, 100);
}
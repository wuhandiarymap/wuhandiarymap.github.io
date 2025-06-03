let meta_data;

const dateInput = document.getElementById("datepicker");
const mapFrame = document.getElementById("map");
const date = document.getElementById("date");
const checkbox = document.getElementById("checkbox");
const title = document.getElementById("title");
const source = document.getElementById("source");
const location_name = document.getElementById("location");
const mentioned = document.getElementById("mentioned");
const mentioned_total = document.getElementById("mentioned_total");
const context = document.getElementById("context");
const description = document.getElementById("description");

fetch("meta_data.json")
    .then(response => {
        return response.json();
    })
    .then(data => {
        meta_data = data;
        updateUI(dateInput.value);
    })

dateInput.addEventListener("change", function() {
    updateUI(this.value);
});

checkbox.addEventListener("change", function() {
    updateUI(dateInput.value);
});

function back() {
    const currentDate = new Date(dateInput.value);
    const minDate = new Date(dateInput.min);
    currentDate.setDate(currentDate.getDate() - 1);
    const nextDate = currentDate.toISOString().split("T")[0];
    if (currentDate >= minDate) {
        dateInput.value = nextDate;
        updateUI(nextDate);
    } else {
        alert("No data for " + nextDate);
    }
}

function next() {
    const currentDate = new Date(dateInput.value);
    const maxDate = new Date(dateInput.max);
    currentDate.setDate(currentDate.getDate() + 1);
    const nextDate = currentDate.toISOString().split("T")[0];
    if (currentDate <= maxDate) {
        dateInput.value = nextDate;
        updateUI(nextDate);
    } else {
        alert("No data for " + nextDate);
    }
}

function updateUI(selectedDate) {
    if (checkbox.checked) {
        mapFrame.src = "maps/" + selectedDate + "_open-street-map.html";
    } else {
        mapFrame.src = "maps/" + selectedDate + "_carto-positron-nolabels.html";
    }

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
                if (data.points[0]["data"]["type"] == "scattermap") {
                    const location_data = data.points[0]["data"]["customdata"];
                    location_name.innerHTML = location_data[0];
                    mentioned.innerHTML = "<b>Mentioned this day: </b>" + location_data[1];
                    mentioned_total.innerHTML = "<b>Mentioned total: </b>" + location_data[2];
                    context.innerHTML = "<b>Context: </b>" + location_data[3];
                    description.innerHTML = "<b>Description: </b>" + location_data[4];
                } else {
                    const index = data.points[0]["pointIndex"];
                    const location_data = data.points[0]["data"]["customdata"][index][0];
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
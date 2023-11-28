function intToString(number){
    result = number.toString();
    if (number < 10){
        result = "0" + result;
    }
    return result;

}

function formatDescription(description){
    if (description != ""){
        description = " - " + description
    }
    return description
}

async function getEvent(eventNumber){
    const result = await fetch(`/date/upcomming/${eventNumber}`);
    result.json().then(data => {
        var eventElement = document.getElementById(`${eventNumber}`);
        
        var dayElement = eventElement.querySelector('.luho_event__day');
        dayElement.textContent = data["start_date"]["day"];
        
        var monthElement = eventElement.querySelector('.luho_event__month');
        monthElement.textContent = data["start_date"]["month_abbreviation"];
        
        var titleElement = eventElement.querySelector('.luho_event__title');
        titleElement.textContent = data["title"];
        
        var descriptionElement = eventElement.querySelector(".luho_event__description");
        descriptionElement.textContent =`
            ${intToString(data["start_time"]["hour"])}:${intToString(data["start_time"]["minute"])}
            ${"Uhr"}
            ${formatDescription(data["description"])}`;

        var categoryElement = eventElement.querySelector(".luho_event__category");
        categoryElement.textContent = data["category"];
        categoryElement.style.setProperty('background-color', data["category_color"], 'important')

    });
}


getEvent(1)
getEvent(2)
getEvent(3)
getEvent(4)
getEvent(5)
getEvent(6)
getEvent(7)
getEvent(8)
getEvent(9)
getEvent(10)
getEvent(11)
getEvent(12)


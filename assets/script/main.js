

async function getEvent(eventNumber){
    const result = await fetch(`/event/upcomming/${eventNumber}`);
    result.json().then(data => {
        var eventElement = document.getElementById(`${eventNumber}`);
        
        var dayElement = eventElement.querySelector('.luho_event__day');
        dayElement.textContent = data["start_date"]["day"];
        
        var monthElement = eventElement.querySelector('.luho_event__month');
        monthElement.textContent = data["start_date"]["month"];
        
        var titleElement = eventElement.querySelector('.luho_event__title');
        titleElement.textContent = data["title"];
        
        var descriptionElement = eventElement.querySelector(".luho_event__description");
        descriptionElement.textContent = `${data["start_time"]["hour"]}:${data["start_time"]["minute"]} - ${data["description"]}`;

        var categoryElement = eventElement.querySelector(".luho_event__category");
        categoryElement.textContent = data["category"];

    });
}


getEvent(1)
getEvent(2)
getEvent(3)


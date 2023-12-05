function intToString(number){
    result = number.toString();
    if (number < 10){
        result = "0" + result;
    }
    return result;

}

function formatDescription(description, speaker="", sermontext=""){
    if (description != ""){
        description = " - " + description;
    }
    if (speaker != ""){
        if (description == ""){
            description = description + " - ";
        }
        description = description + " mit " + speaker;
    }
    if (sermontext != ""){
        if (description != ""){
            description = description + " - "
        }
        description = description + " Bibeltext: " + sermontext;
    }
    return description;
}

var livestreamHTML =    `<span class="luho_event__livestream">
                            <img style="padding: 0px; width:80px;height:80px;" src="../icons/livestream.png" alt="Uhr">
                        </span>`;
var childrenchurchHTML =    `<span class="luho_event__childrenchurch">
                                <img style="padding-top: 0px; padding-bottom: 0px; width:80px;height:80px;" src="../icons/children.png" alt="mit Kinderkirche">
                            </span>`;

var communionHTML = `<span class="luho_event__communion">
                        <img style="padding-top: 0px; padding-bottom: 0px; width:80px;height:80px;" src="../icons/communion.png" alt="mit Abendmahl">
                    </span>`

function locationHTML(location="Location"){
    return `<span class="luho_event__location">
                <img style="padding-top: 15px; padding-bottom: 15px; width:50px;height:80px;" src="../icons/location.svg" alt="Ort:">
                <span class="luho_event__location" style="
                            align-self: flex-start;
                            font-size: 40px;
                            display: inline-block;
                            margin: 15px 0; 
                            padding-left: 0px; 
                            padding-right: 0px;">
                    ${location}
                </span>
            </span>`;
}

function categoryHTML(category="Kategorie", backgroundColor="#0560ab"){
    if (backgroundColor == ""){
        backgroundColor="#0560ab";
    }
    return `<span class="luho_event__category" style="background-color: ${backgroundColor}" >
                ${category}
            </span>`;
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
        descriptionElement.innerHTML =`
            ${intToString(data["start_time"]["hour"])}:${intToString(data["start_time"]["minute"])}
            ${"Uhr"}
            ${formatDescription(data["description"], speaker=data["speaker"], sermontext=data["sermontext"])}`;

        //var categoryElement = eventElement.querySelector(".luho_event__category");
        //categoryElement.textContent = data["category"];
        //categoryElement.style.setProperty('background-color', data["category_color"], 'important')

        var infoElement = eventElement.querySelector(".luho_event__info");
        // Set Category if there is information about the Category
        if (data["category"] != ""){
            infoElement.innerHTML += categoryHTML(data["category"], data["category_color"])
        }
        
        // TODO Sermontext

        // TODO Speaker

        // Set Livestream Icon
        if (data["has_livestream"]){
            infoElement.innerHTML += livestreamHTML
        }

        // Set Childrenschurch Icon
        if (data["has_childrenschurch"]){
            infoElement.innerHTML += childrenchurchHTML
        }

        // Set Communion Icon
        if (data["has_communion"]){
            infoElement.innerHTML += communionHTML
        }

        // Set Location if there is information about the Location
        if (data["location"] != ""){
            infoElement.innerHTML += locationHTML(data["location"])
        }

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


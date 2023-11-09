importScripts 

function resolveMessage(messageBytes){
    message = 
    //TODO
}


function resolveColor(){


}

function sleep(milliseconds) {
    return new Promise(resolve => setTimeout(resolve, milliseconds));
}


async function setScreenColor(r, g, b){
    let screen = document.getElementById("color-screen");

    screen.style.transitionProperty = "all";
    screen.style.transitionTimingFunction = "linear";
    screen.style.transitionDuration = "5s";
    screen.style.backgroundColor = "rgb(" + r + "," + g + "," + b + ")";
    
    await sleep(5000);
    
    setScreenColor(g,b,r);

}

setScreenColor(255,0,0);


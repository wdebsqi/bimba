function getStops() {
    // Gets available stops data from the REST API

    let HOST = window.location.href.split(':', 2).join(':')
    let REST_API_PORT = '5001'

    let options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify({
            'properties': ['stop_name'],
            'distinct': true,
            'ordered': true,
            'ordered_by': ['stop_name']
        })
}
    fetch(`${HOST}:${REST_API_PORT}/stops`, options)
        .then(res => res.json())
        .then(d => { stops = d})
};

function clearInput(inputVal) {
    // Clears the input value from unwanted characters

    // remove all non-alphanumeric characters, but leave spaces, dots and dashes
    let clean = inputVal.replace(/[^\w\s\.-ąęółąńśżź]/gim, '')
    // remove excessive dashes
    clean = clean.replace(/-{2,}/gim, '-')
    // remove excessive dots
    clean = clean.replace(/\.{2,}/gim, '.')
    // remove excessive spaces
    clean = clean.replace(/\s{2,}/gim, ' ')
    return clean
}

function filterStops(stopsArr, inputVal) {
    // Filters stops array based on the input value

    let inputValClean = clearInput(inputVal).replace('.', '\\.')
    // inputValClean = inputValClean.replace('.', '\\.')
    let re = new RegExp(inputValClean, 'gmi')
    return stopsArr.filter(name => name.match(re))
}

function removeOpenLists() {
    // Removes input lists from the DOM
    
    currentFocus = -1
    let stopsItems = document.getElementsByClassName('stops-items')
    for (let i = 0; i < stopsItems.length; i++) {
        stopsItems[i].parentNode.removeChild(stopsItems[i])
    }
}

function modifyMatchedText(text, pattern) {
    // Modifies the text to highlight which part matches the pattern

    let textLowered = text.toLowerCase()
    pattern = clearInput(pattern).toLowerCase()

    let startIdx = textLowered.indexOf(pattern)
    let endIdx = startIdx + pattern.length - 1

    return text.slice(0, startIdx)
            + '<u>'
            + text.slice(startIdx, endIdx + 1)
            + '</u>'
            + text.slice(endIdx + 1, text.length)
}

function markActive(stopItems) {
    // Marks the active item in the stops list
    
    if (!stopItems) return false
    unmarkActive(stopItems)

    if (currentFocus >= stopItems.length) currentFocus = 0
    if (currentFocus < 0) currentFocus = (stopItems.length - 1)

    stopItems[currentFocus].classList.add('stop-item-active')
}

function unmarkActive(stopItems) {
    // Unmarks all items in the stops list

    for (let i = 0; i < stopItems.length; i++) {
        stopItems[i].classList.remove('stop-item-active')
    }
}

function updateStopsList(inputField) {
    // Updates the input field with the proper stops list

    removeOpenLists()
    if (inputField.value.length >= 3) {
        let filteredStops = filterStops(stops, inputField.value)

        let stopsListDiv = document.createElement('div')
        stopsListDiv.setAttribute('id', inputField.id + '-stops-list')
        stopsListDiv.setAttribute('class', 'stops-items')

        inputField.parentNode.appendChild(stopsListDiv)

        for (i = 0; i < filteredStops.length; i++) {
            let stopDiv = document.createElement('div')
            stopDiv.innerHTML += modifyMatchedText(filteredStops[i], inputField.value)
            stopDiv.innerHTML += '<input type="hidden" value="' + filteredStops[i] + '">'
            stopDiv.addEventListener('click', function (e) {
                inputField.value = this.getElementsByTagName('input')[0].value
                removeOpenLists()
            })
            stopsListDiv.appendChild(stopDiv)
        }
    }
}

function moveOnStopsList(inputField, event) {
    // Moves up and down the stops list. Also allows selecting and closing the list
    
    let stopItems = document.getElementById(inputField.id + '-stops-list')
    if (stopItems) {
        stopItems = stopItems.getElementsByTagName("div")
    }
    if (event.key == 'ArrowDown') {
        currentFocus++
        markActive(stopItems)
    } else if (event.key == 'ArrowUp') {
        currentFocus--
        markActive(stopItems)
    } else if (event.key == 'Escape') {
        removeOpenLists()
    } else if (event.key == 'Enter') {
        event.preventDefault()
        tmp = stopItems
        if (currentFocus > -1) {
            if (stopItems) stopItems[currentFocus].click()
        }
    }
}

let stops = []
let currentFocus = null
let tmp = null
getStops()

const startStopInput = document.getElementById('startStopInput')
const endStopInput = document.getElementById('endStopInput')

startStopInput.addEventListener('input', () => {
    updateStopsList(startStopInput)
})
startStopInput.addEventListener('touchstart', () => {
    updateStopsList(startStopInput)
})
startStopInput.addEventListener('touchend', () => {
    updateStopsList(startStopInput)
})
endStopInput.addEventListener('input', () => {
    updateStopsList(endStopInput)
})
endStopInput.addEventListener('touchstart', () => {
    updateStopsList(startStopInput)
})
endStopInput.addEventListener('touchend', () => {
    updateStopsList(startStopInput)
})
startStopInput.addEventListener('keydown', function (e) {
    moveOnStopsList(startStopInput, e)
})
endStopInput.addEventListener('keydown', function (e) {
    moveOnStopsList(endStopInput, e)
})

document.addEventListener('click', removeOpenLists)
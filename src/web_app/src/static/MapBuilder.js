class MapBuilder {
    locations = null
    constructor(locations) {
        this.locations = locations;
        this.mapDivId = 'map-container'
    }

    buildMap() {
        Plotly.newPlot(this.mapDivId, this.#getData(), this.#getLayout(), { displayModeBar: false, responsive: true})
    }

    #getLayout() {
        return {
            dragmode: 'zoom',
            mapbox: {
                style: 'open-street-map',
                center: this.#getCenterCoordinates(this.#unpack('lat'), this.#unpack('lon')),
                zoom: this.#getZoomValue()
            },
            margin: { r: 1, t: 1, b: 1, l: 1 }
        }
    }

    #getData() {
        return [ {
            type: 'scattermapbox',
            text: this.#unpack('name'),
            lon: this.#unpack('lon'),
            lat: this.#unpack('lat'),
            locations: this.#unpack('zone'),
            marker: { color: '#0d6efd', size: 8 }
        } ]
    }

    #unpack(key) {
        return this.locations.map(function (location) {
            return location[key]
        })
    }

    #getCenterCoordinates(latArray, lonArray) {
        return {
            lat: this.#getMiddleValue(latArray),
            lon: this.#getMiddleValue(lonArray)
        }
    }

    #getMiddleValue(arr) {
        let idx = Math.floor(arr.length / 2)
        return arr[idx]
    }

    #getZoomValue() {
        const zoomReductionPerStop = 0.05
        const zoomBase = 12
        return zoomBase - (zoomReductionPerStop * this.locations.length)
    }

}
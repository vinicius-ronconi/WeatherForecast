import queryString from 'query-string'
import { API_ENDPOINT_SEARCH_CITIES, API_ENDPOINT_SEARCH_FORECAST } from './constants'

const fetch = window.fetch

export const getCities = (sentence) => {

    const query = queryString.stringify({
        q: sentence
    })

    const options = {
        method: 'GET'
    }

    return fetch(`${API_ENDPOINT_SEARCH_CITIES}?${query}`, options).then(response => {
        if (response.ok) {
            return response.json()
        } else {
            return Promise.reject('error')
        }
    })
}

export const getForecast = (locationId, units = 'C') => {

    const query = queryString.stringify({
        location_id: locationId,
        units: units
    })

    const options = {
        method: 'GET'
    }

    return fetch(`${API_ENDPOINT_SEARCH_FORECAST}?${query}`, options).then(response => {
        if (response.ok) {
            return response.json()
        } else {
            return Promise.reject('error')
        }
    })
}
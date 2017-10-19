import queryString from 'query-string'
import { API_ENDPOINT_SEARCH_CITIES, API_ENDPOINT_SEARCH_FORECAST } from './constants'

const fetch = window.fetch;

export const getCities = (sentence) => {

    const query = queryString.stringify({
        q: sentence
    });

    const options = {
        method: 'GET'
    };

    return fetch(`${API_ENDPOINT_SEARCH_CITIES}?${query}`, options).then(response => {
        let json = response.json();

        if (response.ok) {
            return json
        } else {
            return json.then(Promise.reject.bind(Promise));
        }
    })
};

export const getForecast = (locationId, units = 'C') => {

    const query = queryString.stringify({
        location_id: locationId,
        units: units
    });

    const options = {
        method: 'GET'
    };

    return fetch(`${API_ENDPOINT_SEARCH_FORECAST}?${query}`, options).then(response => {
        let json = response.json();

        if (response.ok) {
            return json
        } else {
            return json.then(Promise.reject.bind(Promise));
        }
    })
};

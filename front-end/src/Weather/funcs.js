import { SUNNY, CLOUDY, RAINY } from './../constants'

function getWeatherType(weather) {

  if (weather.includes('clear')) {
    return SUNNY
  }

  if (weather.includes('clouds') || weather.includes('fog')) {
    return CLOUDY
  }

  return RAINY
}

export { getWeatherType }
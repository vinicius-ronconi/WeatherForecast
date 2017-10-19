import React, { Component } from 'react'
import { Grid } from 'semantic-ui-react'
import { SUNNY, CLOUDY, RAINY } from './../constants'
import { getWeatherType } from './funcs'
import classnames from 'classnames'
import './Weather.css'

const WeatherHeader = ({ city = "", weather = ""}) => (
  <div className="weather-header">
    <div className="weather-place" title="Place">
      {city.name}, {city.country_code}
    </div>
    {weather.description.includes('clear') && (<i className="material-icons weather-icon">wb_sunny</i>)}
    {weather.description.includes('clouds') && (<i className="material-icons weather-icon">wb_cloudy</i>)}
    {weather.description.includes('fog') && (<i className="material-icons weather-icon">wb_cloudy</i>)}
    {weather.description.includes('rain') && (<i className="material-icons weather-icon">flash_on</i>)}
    <div className="weather-temp" title="Temperature">
      {weather.temperature}° C
    </div>
  </div>
)

const WeatherBody = ({ weather = {}}) => (
  <div className="weather-body">
    <Grid columns='three' divided>
      <Grid.Row>
        <Grid.Column title="Humidity">
          <i className="material-icons">filter_drama</i>
          <div className="weather-info">
            {weather.humidity} %
          </div>
        </Grid.Column>
        <Grid.Column title="Wind Speed">
          <i className="material-icons">toys</i>
          <div className="weather-info">
            {weather.wind_speed} m/s
          </div>
        </Grid.Column>
        <Grid.Column title="Pressure">
          <i className="material-icons">filter_hdr</i>
          <div className="weather-info">
            {weather.pressure} hpa
          </div>
        </Grid.Column>
      </Grid.Row>
    </Grid>
  </div>
)

class Weather extends Component {

  render() {
    const { data } = this.props

    const compStyle = getWeatherType(data.current_weather.description)
    
    const className = classnames('weather', {
      'weather--sunny': SUNNY === compStyle,
      'weather--rainy': RAINY === compStyle,
      'weather--cloudy': CLOUDY === compStyle,
    })

    return (
      <div className={className}>
        {data && (<WeatherHeader city={data.city} weather={data.current_weather} />)}
        {data && (<WeatherBody weather={data.current_weather} />)}
      </div>
    )
  }
}

export default Weather

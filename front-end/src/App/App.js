import React, { Component } from 'react'
import { getCities, getForecast } from '../api'

//Components
import Weather from './../Weather'
import { Search, Label, Loader, Message } from 'semantic-ui-react'

//Styles
import './App.css'
import 'semantic-ui-css/semantic.min.css'

const resultRenderer = ({ id, name, country, flag_url }) => <Label key={id} content={`${name} - ${country}`} />

const Layout = ({ children }) => (
  <div className="fluid-height aligner">
    <div className="app app--shadow aligner-item">
      {children}
    </div>
  </div>
)

class App extends Component {

  constructor() {
    super();

    this.state = {
      forecast: null,
      error: null
    }
  }

  componentDidMount() {
    this.fetchForecast('6173331')
  }

  componentWillMount() {
    this.resetComponent()
  }

  resetComponent() {
    this.setState({
      isLoading: false,
      cities: [],
      value: ''
    })
  }

  handleResultSelect = (e, { result }) => {
    this.fetchForecast(result.id)
  };

  handleSearchChange = (e, { value }) => {
    this.setState({
        isLoading: true, value
    });

    setTimeout(() => {
      if (this.state.value.length < 1) {
        return this.resetComponent()
      }

      getCities(value).then((data) => {
        this.setState({
          cities: data,
          isLoading: false,
        })
      }).catch((err) => this.handleError(err))
    }, 10)
  };

  fetchForecast = (locationId) => {
    getForecast(locationId).then((data) => {
      this.setState({
        forecast: data
      })
    }).catch((err) => this.handleError(err))
  };

  handleError = (data) => {
    this.setState({
        error: data.error
    })
  }

  render() {
    const { isLoading, value, cities, forecast, error } = this.state

    if (error !== null) {
      return (
        <Layout>
          <div className="app-info">
            <Message negative>
              {error}
            </Message>
          </div>
        </Layout>
      )
    }


    if (forecast == null) {
      return (
        <Layout>
          <div className="app-info">
            <Loader size='medium' active inline='centered'>Loading</Loader>
          </div>
        </Layout>
      )
    }

    return (
      <Layout>
        <div className="header">
          <div className="header-search">
            <Search
              placeholder="Type city name.."
              className="header-search__input"
              loading={isLoading}
              onResultSelect={this.handleResultSelect}
              onSearchChange={this.handleSearchChange}
              results={cities}
              value={value}
              resultRenderer={resultRenderer}
              {...this.props} />
          </div>
        </div>
        <Weather data={this.state.forecast} />
      </Layout>
    )
  }
}

export default App
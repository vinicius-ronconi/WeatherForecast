import React from 'react';
import ReactDOM from 'react-dom';
import registerServiceWorker from './registerServiceWorker';
import App from './App';

const RootApp = () => (
  <App />
);

ReactDOM.render(
  <RootApp />, document.getElementById('root'));

registerServiceWorker();

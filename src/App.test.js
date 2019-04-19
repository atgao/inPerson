import React from 'react';
// import ReactDOM from 'react-dom';
import { render } from 'react-snapshot';
import App from './App';

it('renders without crashing', () => {
  const div = document.createElement('div');
  render(<App />, div)
//   ReactDOM.render(<App />, div);
//   ReactDOM.unmountComponentAtNode(div);
});

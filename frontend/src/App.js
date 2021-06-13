import React, {Component} from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";
import Login from './auth/login.jsx';
import './App.css';
import NavBar from './auth/navbar.jsx';


class App extends Component {
  render(){
    return(
      <Router>
        <div>
          <NavBar />
          <Route exact path="/login" component={Login} />
        </div>
      </Router>
      )
  }
}

export default App;

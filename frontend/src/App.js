// Importing modules
import React, { Component, useState, useEffect } from "react";
import 'tachyons';
import Logo from "./Components/Logo/Logo";
import GrabUser from "./Components/GrabUser/GrabUser";
import UserInput from "./Components/UserInput/UserInput";
 
const backEndURL = "http://127.0.0.1:5000/";

class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
       username: "",
       taste: []
    };
  }

  onUserChange = (name) => {
    this.setState({username: name});
  }

  onSubmit = () => {
    fetch(backEndURL)
    .then((response) => response.json())
    .then(responseJSON => console.log(responseJSON))
    .then((data) => {console.log(data)})
    .catch((error) => {console.log("We had an error: " + error)})
  }

render() {
      return (
        <div className="App">
          <link rel="preconnect" href="https://fonts.googleapis.com" />
          <link rel="preconnect" href="https://fonts.gstatic.com" />
          <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap" rel="stylesheet" />

          <Logo />
          <div>
            <UserInput onUserChange={this.onUserChange} /><br/><br/>
          </div>
            <GrabUser onSubmit={this.onSubmit} />
          {
            /**
             * TODO:
             * 
             * <GrabUser /> // Will get the user whose tastes will be used
             * <Mood />     // Allows the user to input a mood for the playlist
             * <Logo />     // Site logo
             * 
             */
          }
        </div>
    );
  }
}

export default App;
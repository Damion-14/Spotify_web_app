// Importing modules
import React, { Component, useState, useEffect } from "react";
import 'tachyons';
import "./App.css";
import Logo from "./Components/Logo/Logo";
import GrabUser from "./Components/GrabUser/GrabUser";
 
class App extends Component {
    // usestate for setting a javascript
    // object for storing and using data
    constructor(props) {
      super(props);
      this.state = {
        username: "",
      };
    }
 
render() {
      return (
        <div className="App">
          <link rel="preconnect" href="https://fonts.googleapis.com" />
          <link rel="preconnect" href="https://fonts.gstatic.com" />
          <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap" rel="stylesheet" />
          <Logo />
          <GrabUser />
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
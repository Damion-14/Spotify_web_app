// Importing modules
import React, { Component, useState, useEffect } from "react";
import 'tachyons';
import Logo from "./Components/Logo/Logo";
import UserInput from "./Components/UserInput/UserInput";
import home from "./Components/pages/home";
 
// const backEndURL = "http://127.0.0.1:5000/"; // For Frontend testing purposes

const url = "http://192.168.1.180:8000";
const params = new URLSearchParams({
  client_id: "779617d6c75e425992d9aad1336fc8e4",
  client_secret: "a9b25d041321424b8b9ddbbb804ab80e",
  username: "Damion"
});

class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
       username: "",
       taste: [],
       isSignedIn: false,
       currentPage: 'sign-in'
    };
  }

  // Below are the methods used to interact with the backend/server
  LOGIN() {
    this.onRouteChange('home');

    fetch(url, {
      method: 'POST',
      body: params,
    })
      .then(response => response.json())
      .then(data => {
        if(data) {
          this.setState({isSignedIn: true});
        }
        console.log(data);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }

//GET QUEUE

GET_QUEUE() {
  const get_queue = url + "/get_queue";

  const get_queue_params = new URLSearchParams({
    client_id: "779617d6c75e425992d9aad1336fc8e4"
  });

  fetch(get_queue, {
    method: 'POST',
    body: get_queue_params,
  })
    .then(response => response.json())
    .then(data => {
      const x = data;
      console.log(x);
    })
    .catch(error => {
      console.error('Error:', error);
    });
}


//NEW PLAYLIST
NEW_PLAYLIST() {
  const new_playlist = url + "/new_playlist";
  // Define the payload (data) to send in the POST request
  const new_playlist_params = {
    client_id: "779617d6c75e425992d9aad1336fc8e4",
    name: "fastapi1",
    add_songs_flag: true,
    seed_artists: null,
    seed_genres: null,
    seed_tracks: "4daEMLSZCgZ2Mt7gNm2SRa,  2WqTKOAUmv7hz9ZzGnXHrY",
    limit: 20,
    number_of_songs_to_add: 30
  };

  fetch(new_playlist, {
    method: 'POST',
    body: new URLSearchParams(new_playlist_params),
  })
    .then(response => response.json())
    .then(data => {
      console.log(data);
    })
    .catch(error => {
      console.error('Error:', error);
    });

}

// *************************************************************************

  onUserChange = (name) => {
    this.setState({username: name});
  }

  onRouteChange = (route) => {
    if(route === 'home') {
      this.setState({isSignedIn: true, currentPage: 'home'});
    }
    else if(route === 'queue') {
      this.setState({currentPage: 'queue'})
    }
  }

  onSubmit = () => {

    this.LOGIN();
    /*
    fetch(backEndURL)
    .then((response) => response.json())
    .then(responseJSON => console.log(responseJSON))
    .then((data) => {console.log(data)})
    .catch((error) => {console.log("We had an error: " + error)})*/
  }

render() {
      return (
        <div className="App">
          <link rel="preconnect" href="https://fonts.googleapis.com" />
          <link rel="preconnect" href="https://fonts.gstatic.com" />
          <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap" rel="stylesheet" />\
          {
            this.state.isSignedIn === false 
            ? 
              //Sign in page
              <div className="Sign-in">
                <Logo />
                <UserInput onUserChange={this.onUserChange} onSubmit={this.onSubmit} />
              </div>
            :
              // Homepage
              <div className="Home">
                <h1> Welcome! </h1>
              </div>
          }
        </div>
    );
  }
}

export default App;
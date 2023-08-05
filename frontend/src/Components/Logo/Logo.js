import React from 'react';
import { Component } from 'react';
import 'tachyons';
import Tilt from 'react-parallax-tilt';
import './Logo.css';
import logo from './logo.png';

const Logo = () => {
    return (
        <div>
            <div height="auto" width="150px">
                <Tilt tiltEnable={false} display='inline-block'>
                  <div /*onClick={//onRouteChange('home')}*/ border="auto" className="ml2 mt2 w4 h4 tc" style={{
                       display: 'inline-block',
                       border: '3px solid black',
                    }}
                    >
                      <img height="auto" width="100px" alt="logo.png" src={logo} />
                    </div>
                </Tilt>
            </div>
            <h1 className="tc" font-size="100%">Welcome to the House Party!</h1>
        </div>
    );
}

export default Logo;
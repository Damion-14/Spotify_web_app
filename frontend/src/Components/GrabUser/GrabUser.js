import React from 'react';
import { Component } from 'react';
import 'tachyons';
import './GrabUser.css';

const GrabUser = ({onSubmit}) => {
    return (
        <div className="dial-button" htmlFor="dial" style={{
            "--kids": 1,
            "--radius": 40,
            "--offset": 25,
            "--bounds": 360,
            "--delay": 0,
            "--transition": 0.2,
            "--child": 44,
            "--parent": 56
        }}>
            <input type="checkbox" id="dial" />
            <button className="dial-button" style={{ "--index": 0 }} onClick={onSubmit}>0</button>
            <button style={{ "--index": 1 }} onClick={onSubmit}>1</button>
            <button style={{ "--index": 2 }} onClick={onSubmit}>2</button>
            <button style={{ "--index": 3 }} onClick={onSubmit}>3</button>
            <button style={{ "--index": 4 }} onClick={onSubmit}>4</button>
            <label htmlFor="dial">
                <svg viewBox="0 0 24 24">
                    <path d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"></path>
                </svg>
            </label>
            <label className="dial-button__cloak" htmlFor="dial">
            </label>
       </div>
    );
}

export default GrabUser;
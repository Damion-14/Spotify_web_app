import React from 'react';
import 'tachyons';
import './UserInput.css';

const UserInput = ({onUserChange, onSubmit}) => {
    return (
        <div className="tc">
            <label htmlFor="inputBox">Enter your username:</label><br/>
            <input width="200px" height="1000px" id="inputBox" onChange={(event) => { onUserChange(event.target.value) }} type="text" />
            <br/>
            <br/>
            <button className='submit' type='submit' onClick={onSubmit}>Submit</button>
        </div>
    );
}

export default UserInput;
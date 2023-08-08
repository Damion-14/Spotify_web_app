import React from 'react';
import 'tachyons';

const GrabUser = ({onSubmit, onUserChange}) => {
    return(
        <div className="tc">
            <label>Enter your username:</label>
            <input onChange={(event) => {onUserChange(event.target.value)}} type="text"/>
            <button onClick={onSubmit} type="submit">Submit</button>
        </div>
    );
}

export default GrabUser;
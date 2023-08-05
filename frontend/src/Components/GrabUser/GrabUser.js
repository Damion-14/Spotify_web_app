import React from 'react';
import 'tachyons';

const GrabUser = () => {
    return(
        <div className="tc">
            <label>Enter your username:</label>
            <input type="text"/>
            <button type="submit">Submit</button>
        </div>
    );
}

export default GrabUser;
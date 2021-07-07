import React from 'react';
import Navigation from './components/Navigation/Navigation';
import { Redirect } from 'react-router-dom';

import './App.css';

const App = () => {
    return (
        <>
            <Navigation/>
            <Redirect to="/rent" />
        </>
    )
}

export default App;

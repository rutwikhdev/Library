import React from 'react';
import { Switch, Route, Link } from 'react-router-dom';

import Rent from '../Rent/Rent';
import Members from '../Members/Members';
import Returns from '../Returns/Returns';
import Transaction from '../Transaction/Transaction';
import Report from '../Report/Report';

import classes from './Navigation.module.css';

const Navigation = () => {
    return (
        <React.Fragment>
            <div className={classes.header}>
                <nav className={classes.nav}>
                    <Link to="/rent" className={classes.links}>Rent</Link>
                    <Link to="/returns" className={classes.links}>Returns</Link>
                    <Link to="/members" className={classes.links}>Members</Link>
                    <Link to="/transaction" className={classes.links}>Transaction</Link>
                    <Link to="/report" className={classes.links}>Reports</Link>
                </nav>
            </div>
            <div className={classes.render_bottom}>
                <Switch>
                    <Route path='/rent'>
                        <Rent />
                    </Route>
                    <Route path='/returns'>
                        <Returns />
                    </Route>
                    <Route path='/members'>
                        <Members />
                    </Route>
                    <Route path='/transaction'>
                        <Transaction />
                    </Route>
                    <Route path='/report'>
                        <Report />
                    </Route>
                </Switch>
            </div>
        </React.Fragment>
    );
}

export default Navigation;

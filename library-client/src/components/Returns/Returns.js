import axios from 'axios';
import React, { useEffect, useState } from 'react';

import classes from '../Members/Members.module.css';
import styles from './Returns.module.css';

const Returns = () => {
    const [rentalData, setRentalData] = useState([]);

    const getRentalsData = async () => {
        await axios.get('http://localhost:5000/get_rentals').then(res => {
            console.log(res);
            setRentalData(res.data);
        }).catch(err => {
            console.log(err);
        })
    }

    const returnHandler = async (memId, bId, i) => {
        await axios.post('http://localhost:5000/return_book', {
            memberID: memId,
            bookID: bId
        }).then(res => {
            console.log(res);
            let newRentals = [...rentalData]
            newRentals[i].rental_status = true
            setRentalData(newRentals)
        }).catch(err => {
            console.log(err);
        })
    };

    var rentals = <tr></tr>
    if (Object.keys(rentalData).length > 0) {

        rentals = Object.values(rentalData).map((el, i) => {
            return (
                <tr>
                    <td>{el.memberID}</td>
                    <td>{el.bookID}</td>
                    <td>{el.rental_status ? 'Returned' : 'Not Returned'}</td>
                    <td>{el.date}</td>
                    {el.rental_status ?
                        <td className={styles.disabledBtn}>Returned</td> :
                        <td className={styles.returnBtn} onClick={() => returnHandler(el.memberID, el.bookID, i)}>Return</td>
                    }
                </tr>
            );
        });
    }

    useEffect(() => {
        getRentalsData();
    }, []);

    return (
        <React.Fragment>
            <p className={styles.title}>Rentals</p>
            <table>
                <tbody>
                    <tr>
                        <td className={classes.tableHeaders}>Member Id</td>
                        <td className={classes.tableHeaders}>Book Id</td>
                        <td className={classes.tableHeaders}>Status</td>
                        <td className={classes.tableHeaders}>Rented on</td>
                        <td className={classes.tableHeaders}>Return</td>
                    </tr>
                    {rentals}
                </tbody>
            </table>
        </React.Fragment>
    );
}

export default Returns
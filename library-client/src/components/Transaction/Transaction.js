import React, { useEffect, useState } from 'react';

import classes from '../Rent/Rent.module.css';
import classes2 from '../Members/Members.module.css';
import styles from './Transaction.module.css';
import axios from 'axios';

const Transaction = () => {
    const [memberId, setMemberId] = useState("");
    const [memberName, setMemberName] = useState("");
    const [amount, setAmount] = useState();
    const [transactions, setTransactions] = useState([]);

    const memberIdHandler = (e) => {
        e.preventDefault();
        setMemberId(e.target.value);
    }

    const memberNameHandler = (e) => {
        e.preventDefault();
        setMemberName(e.target.value);
    }

    const amountHandler = (e) => {
        e.preventDefault();
        setAmount(e.target.value);
    }

    // make transaction
    const transactionHandler = async () => {
        await axios.post('http://localhost:5000/make_transaction', {
            memberID: memberId,
            amount: amount,
            memberName: memberName
        }).then(res => {
            console.log(res);
        }).catch(err => {
            console.log(err);
            alert('Error, enter correct transaction value or memberID');
        });

    }

    // get all transactions
    const getTransactions = async () => {
        await axios.get('http://localhost:5000/get_transactions').then( res => {
            console.log(res);
            setTransactions(res.data);
        }).catch(err => {
            console.log(err);
        })
    }

    var transactionsList = <tr></tr>
        if (Object.keys(transactions).length > 0) {

            transactionsList = Object.values(transactions).map(el => {
                return (
                    <tr>
                        <td>{el.memberID}</td>
                        <td>{el.memberName}</td>
                        <td>{el.amount}</td>
                        <td>{el.date}</td>
                        <td>{el.time}</td>
                        <td>{el.status}</td>
                    </tr>
                );
            });
        }

    useEffect(() => {
        getTransactions();
    }, [])

    return (
        <React.Fragment>
            <form className={styles.transactionForm} onSubmit={transactionHandler}>
                <input
                    type="text"
                    value={memberId}
                    onChange={memberIdHandler}
                    className={classes.inputField}
                    placeholder="Member ID"
                    required
                />
                <input
                    type="text"
                    value={memberName}
                    onChange={memberNameHandler}
                    className={classes.inputField}
                    placeholder="Member Name"
                    required
                />
                <input
                    type="text"
                    value={amount}
                    onChange={amountHandler}
                    className={classes.inputField}
                    placeholder="Amount"
                    required
                />
                <button className={classes.btn}>Pay</button>
            </form>

            <table>
                <tbody>
                    <tr>
                        <td className={classes2.tableHeaders}>Member Id</td>
                        <td className={classes2.tableHeaders}>Name</td>
                        <td className={classes2.tableHeaders}>Amount(in ₹)</td>
                        <td className={classes2.tableHeaders}>Date</td>
                        <td className={classes2.tableHeaders}>Time</td>
                        <td className={classes2.tableHeaders}>Status</td>
                    </tr>
                    {transactionsList}
                </tbody>
            </table>
        </React.Fragment>
    );
}

export default Transaction;

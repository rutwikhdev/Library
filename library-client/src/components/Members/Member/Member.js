import React from 'react';
import axios from 'axios';
import classes from './Member.module.css';

const Member = (props) => {

    // Server calls
    // remove member from database
    const deleteMemberHandler = async () => {
        await axios.post('http://localhost:5000/remove_member', {
            id: props.data.id
        }).then(res => {
            // remove member from state
            console.log(res);
            const newMembers = props.stateRef.filter(el => {
                return el.id !== props.data.id;
            })

            props.stateCallback(newMembers)

        }).catch(err => {
            console.log(err);
            alert('Error: Clear outstanding or return books.')
        });
    }

    return (
        <tr className={classes.member}>
            <td className={classes.memberId}>{props.data.id}</td>
            <td className={classes.memberName}>{props.data.name}</td>
            <td className={classes.memberOutstanding}>{props.data.debt}</td>
            <td className={classes.removeBtn} onClick={deleteMemberHandler}>Remove</td>
        </tr>
    );
}

export default Member;

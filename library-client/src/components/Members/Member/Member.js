import React from 'react';
import axios from 'axios';
import classes from './Member.module.css';

const Member = (props) => {
    const deleteMemberHandler = async () => {
        if (props.data.debt > 0) {
            alert('Clear outstanding first');
            return
        }
        
        // remove member from database
        await axios.post('http://localhost:5000/remove_member', {
            id: props.data.id
        }).then(res => {
            console.log(res);
        }).catch(err => {
            console.log(err);
        });

        // remove member from state
        const newMembers = props.stateRef.filter(el => {
            return el.id !== props.data.id;
        })

        props.stateCallback(newMembers)
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
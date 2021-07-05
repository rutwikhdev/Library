import React, { useState, useEffect } from 'react';
import axios from 'axios';

import Member from './Member/Member';

import classes from './Members.module.css';
import classes2 from '../Rent/Rent.module.css';

const Members = () => {
    const [name, setName] = useState("");
    const [members, setMembers] = useState([]);

    // Input Handlers
    const nameChangeHandler = (e) => {
        e.preventDefault();
        setName(e.target.value);
    }

    // Server calls
    // add member to database
    const addMemberHandler = async () => {
        await axios.post('http://localhost:5000/add_member', {
            name: name
        }).then(res => {
            console.log(res);
        }).catch(err => {
            console.log(err);
        });
    }

    // get members from database
    const fetchMembers = async () => {
        const res = await axios.get('http://localhost:5000/get_members');
        setMembers(res.data);
    };

    useEffect(() => {
        fetchMembers();
    }, []);

    var renderMembers = <tr className={classes.members}></tr>;
    if (Object.keys(members).length > 0) {

        renderMembers = Object.values(members).map(el => {
            return (
                <Member
                    data={el}
                    stateRef={members}
                    stateCallback={setMembers} />
            );
        });
    }

    return (
        <React.Fragment>
            <form onSubmit={addMemberHandler} className={classes.memberForm}>
                <input
                    type='text'
                    value={name}
                    onChange={nameChangeHandler}
                    className={classes2.inputField}
                    placeholder='Enter member name'
                    required
                />
                <button className={classes2.btn}>Add Member</button>
            </form>
            <table>
                <tbody>
                    <tr>
                        <td className={classes.tableHeaders}>Unique Id</td>
                        <td className={classes.tableHeaders}>Full Name</td>
                        <td className={classes.tableHeaders}>Current Outstanding</td>
                        <td className={classes.tableHeaders}>Cancel Membership</td>
                    </tr>
                    {renderMembers}
                </tbody>
            </table>
        </React.Fragment>
    );
}

export default Members;

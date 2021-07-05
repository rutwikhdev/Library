import axios from 'axios';
import React, { useState } from 'react';
import PortModal from '../PortModal/PortModal';

import classes from './Book.module.css';
import classes2 from '../Rent.module.css';

const Book = (props) => {
    const [modal, setModal] = useState(false);
    const [memberId, setMemberId] = useState("");

    // Input and Modal state Handlers
    const inputHandler = (e) => {
        e.preventDefault();
        setMemberId(e.target.value);
    }

    const openModal = async () => {
        setModal(true);
    }

    const closeModalHandler = () => {
        setModal(false)
    }

    // Server calls
    // Import books to library
    const addToLibraryHandler = async () => {
        await axios.post('http://localhost:5000/add_library',
            props.data
        ).then(res => {
            console.log(res);
            alert('Successfully added 10 books to the library');
        }).catch(err => {
            console.log(err);
            alert('Some unknown error occurred.')
        });
    }

    // Try renting a book for member using modal
    const rentBookHandler = async () => {
        await axios.post('http://localhost:5000/rent_book', {
            bookID: props.data.bookID,
            memberID: memberId
        }).then(res => {
            console.log(res);
            alert('Successfully rented');
        }).catch(err => {
            console.log(err);
            alert('Outstanding balance too high or already rented.');
        })
        closeModalHandler();
    }

    return (
        <div className={classes.book}>
            {
                modal && (
                    <PortModal
                        bookId={props.data.bookID}
                        title={props.data.title}
                        inputValue={memberId}
                        inputHandler={inputHandler}
                        backdropClick={closeModalHandler}
                        onConfirm={rentBookHandler} />
                )
            }
            <div className={classes.book_details}>
                <div className={classes.book_title}>
                    {props.data.title}
                </div>
                <div className={classes.book_authors}>
                    Authors: {props.data.authors}
                </div>
                <div className={classes.book_publisher}>
                    Publisher: {props.data.publisher}
                </div>
                <div className={classes.book_lang}>
                    Language: {props.data.language_code}, Rating: {props.data.average_rating}
                </div>
                <div className={classes.book_quantity}>Quantity: {props.data.quantity || 10}</div>
            </div>
            <div className={classes.actions}>
                {
                    props.btntype === 'api' ?
                        <button className={`${classes.rent_btn} ${classes2.btn}`} onClick={addToLibraryHandler}>Add to Library</button> :
                        <button className={`${classes.rent_btn} ${classes2.btn}`} onClick={openModal}>Rent</button>
                }
            </div>
        </div>
    );
}

export default Book;

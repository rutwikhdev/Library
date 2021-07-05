import React, { useState } from 'react';
import axios from 'axios';

import classes from './Rent.module.css';
import Book from './Book/Book';

const Rent = () => {
    const [searchText, setSearchText] = useState("");
    const [searchType, setSearchType] = useState("");
    const [searchPlace, setSearchPlace] = useState("");
    const [btnText, setBtnText] = useState("");
    const [books, setBooks] = useState([]);

    // Input handlers
    const searchTextHandler = (e) => {
        e.preventDefault();
        setSearchText(e.target.value);
    }

    const searchTypeHandler = (e) => {
        setSearchType(e.target.value);
    }

    const searchPlaceHandler = (e) => {
        setSearchPlace(e.target.value);
        setBooks([]);
    }

    // Server calls
    // Search book in local db or api
    const searchBook = async (e) => {
        e.preventDefault();
        await axios.post(`http://localhost:5000/search_${searchPlace}`, {
            type: searchType,
            text: searchText
        }).then(res => {
            setBtnText(searchPlace)
            setBooks(res.data)
        }).catch(err => {
            setBooks([])
            console.log(err)
        });
    }

    // Render books dynamically
    var searchedBooks = <div className={classes.results}>No results.</div>;
    if (Object.keys(books).length > 0) {

        searchedBooks = Object.values(books).map(el => {
            return (
                <Book
                    key={el.isbn13 || el.bookID}
                    data={el}
                    btntype={btnText}
                />
            );
        });
    }

    return (
        <React.Fragment>
            <form onSubmit={searchBook} className={classes.search_form}>
                <div>
                    <input
                        type='text'
                        value={searchText}
                        onChange={searchTextHandler}
                        className={classes.inputField}
                        placeholder='Enter author name or title'
                        required
                    />
                    <div className={classes.radio_block}>

                        <div className={classes.block_component}>
                            <div>
                                <input
                                    type='radio'
                                    name='author_title'
                                    id='author'
                                    value='authors'
                                    onChange={searchTypeHandler}
                                    required
                                />
                                <label htmlFor='author'>Author</label>
                            </div>
                            <div>
                                <input
                                    type='radio'
                                    name='author_title'
                                    id='title'
                                    value='title'
                                    onChange={searchTypeHandler}
                                    required
                                />
                                <label htmlFor='title'>Title</label>
                            </div>
                        </div>

                        <div className={classes.block_component}>
                            <div>
                                <input
                                    type='radio'
                                    name='local_api'
                                    id='local'
                                    value='local'
                                    onChange={searchPlaceHandler}
                                    required
                                />
                                <label htmlFor='local'>Local</label>
                            </div>
                            <div>
                                <input
                                    type='radio'
                                    name='local_api'
                                    id='master'
                                    value='api'
                                    onChange={searchPlaceHandler}
                                    required
                                />
                                <label htmlFor='master'>Master(API)</label>
                            </div>
                        </div>

                    </div>
                </div>
                <button className={classes.btn}>Search</button>
            </form>

            {searchedBooks}
        </React.Fragment>
    );
}

export default Rent;

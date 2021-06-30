import React from 'react';
import ReactDOM from 'react-dom';

import styles from './PortModal.module.css';

const Backdrop = props => {
    return <div className={styles.backdrop} onClick={props.backdropClick} />;
}

const ModalOverlay = props => {
    return (
        <div className={styles.modal}>
            <header className={styles.header}>
                <h4>Book ID: {props.bookId}</h4>
            </header>
            <div className={styles.content}>
                <p>Title: {props.message}</p>
                <input
                    type="text"
                    className={styles.input}
                    value={props.inputValue}
                    onChange={props.inputHandler}
                    placeholder="Enter Member ID" />
            </div>
            <footer className={styles.actions}>
                <button className={styles.button} onClick={props.onConfirm}>Rent Request</button>
            </footer>
        </div>
    );
}

const PortModal = props => {
    return (
        <React.Fragment>
            {
                ReactDOM.createPortal(
                    <Backdrop backdropClick={props.backdropClick} />,
                    document.getElementById('backdrop-root')
                )
            }
            {
                ReactDOM.createPortal(
                    <ModalOverlay
                        bookId={props.bookId}
                        message={props.title}
                        inputValue={props.inputValue}
                        inputHandler={props.inputHandler}
                        backdropClick={props.backdropClick}
                        onConfirm={props.onConfirm} />,
                    document.getElementById('overlay-root')
                )
            }
        </React.Fragment>
    )
};

export default PortModal;
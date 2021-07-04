import React, { useEffect, useState } from 'react';
import axios from 'axios';
import jsPDF from 'jspdf';
import * as htmlToImage from 'html-to-image';
import { toPng, toJpeg, toBlob, toPixelData, toSvg } from 'html-to-image';
import download from 'downloadjs';

import Chart from './Chart/Chart';
import classes from './Report.module.css';

const Report = () => {
    const [reports, setReports] = useState({ most_rented: [], most_paid: [], monthly: [] });

    // get all report data
    const getReports = async () => {
        await axios.get('http://localhost:5000/get_reports').then(res => {
            console.log(res);
            setReports(res.data);
        }).catch(err => {
            console.log(err);
        });
    }

    // download pdf or jpeg of reports
    const downloadReports = () => {
        htmlToImage.toJpeg(document.getElementById('capture'), { quality: 0.95,backgroundColor: 'white' })
            .then(function (dataUrl) {
                var link = document.createElement('a');
                link.download = 'my-image-name.jpeg';
                const pdf = new jsPDF();

                const imgProps= pdf.getImageProperties(dataUrl);
                const pdfWidth = pdf.internal.pageSize.getWidth();
                const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

                //download(dataUrl, 'repots.jpeg');
                //pdf.addImage(dataUrl, 'JPEG', 0, 0,pdfWidth, pdfHeight);
                pdf.addImage(dataUrl, 'JPEG', 30, 0, 150, 300)
                pdf.save("reports.pdf");
            });
    }

    var rented_labels = Object.values(reports.most_rented).map(el => {
        return el.authors;
    });

    var rented_data = Object.values(reports.most_rented).map(el => {
        return el.count;
    });

    var member_labels = Object.values(reports.most_paid).map(el => {
        return el.name;
    })

    var amount_data = Object.values(reports.most_paid).map(el => {
        return el.amount;
    });

    var monthly_paid_labels = Object.values(reports.monthly).map(el => {
        return el.month;
    });

    var monthly_paid_data = Object.values(reports.monthly).map(el => {
        return el.amount;
    });

    var renderedBookReports = <tr></tr>;
    if (Object.keys(reports.most_rented).length > 0) {

        renderedBookReports = Object.values(reports.most_rented).map((el, index) => {
            return (
                <tr>
                    <td>{index + 1}</td>
                    <td className={classes.leftAlign}>{el.title}</td>
                    <td>{el.count}</td>
                </tr>
            );
        });
    }

    useEffect(() => {
        getReports()
    }, [])

    return (
        <React.Fragment>
            <button onClick={downloadReports}>Download</button>
            <div id="capture">
                <p className={classes.title}>Top 10 books.</p>
                <table>
                    <tr>
                        <td className={classes.tableHeaders}>No.</td>
                        <td className={classes.tableHeaders}>Book Name</td>
                        <td className={classes.tableHeaders}>Times Rented</td>
                    </tr>
                    {renderedBookReports}
                </table>

                <Chart title={'Top Authors'} labels={rented_labels.slice(0,5)} data={rented_data.slice(0,5)} type={'line'} />
                <Chart title={'Highest Paying Customers'} labels={member_labels} data={amount_data} type={'bar'} />
                <Chart title={'Highest Payment Months'} labels={monthly_paid_labels} data={monthly_paid_data} type={'bar'} />
                <div></div>
            </div>
        </React.Fragment>
    );
}

export default Report;

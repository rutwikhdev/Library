import React from 'react';

import { Bar, Line } from 'react-chartjs-2';
import classes from './Chart.module.css';

const Chart = (props) => {
    // Get colors from App.css -- root level
    var r = document.querySelector(':root');
    var rs = getComputedStyle(r);

    const auroraRed = rs.getPropertyValue('--auroraRed');
    const auroraOrange = rs.getPropertyValue('--auroraOrange');
    const auroraYellow = rs.getPropertyValue('--auroraYellow');
    const auroraGreen = rs.getPropertyValue('--auroraGreen');
    const auroraPink = rs.getPropertyValue('--auroraPink');

    // options for charts
    const options = {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        },
        plugins: {
            responsive: true,
            legend: {
                title: true,
                position: 'right',
                display: false,
                labels: {
                    boxWidth: 20,
                    padding: 20,
                    font: {
                        size: 14
                    }
                }
            },
            title: {
                display: true,
                text: props.title,
                font: {
                    size: 26
                },
            }
        }
    }

    var data = {
        labels: props.labels,
        datasets: [
            {
                data: props.data,
                fill: false,
                backgroundColor: [
                    auroraRed,
                    auroraGreen,
                    auroraYellow,
                    auroraPink,
                    auroraOrange
                ],
            },
        ],
        options: options,
    };

    return (
        <div className={classes.canvas}>
            {
                props.type === 'line' ? <Bar data={data} options={options} /> :
                    <Line data={data} options={options} />}
        </div>
    );
}

export default Chart;

import React, { useState, useEffect } from 'react'

import createPlotlyComponent from 'react-plotly.js/factory';
import Plotly from 'plotly.js-basic-dist';  // https://github.com/plotly/react-plotly.js/issues/135
// import Plot from 'react-plotly.js';
const Plot = createPlotlyComponent(Plotly);

interface singlePlotInf {
    x: Array<number>;
    y: Array<number>;
}

class singlePlot {
    x: Array<number> = [];
    y: Array<number> = [];
    constructor() {
        this.x = [0];
        this.y = [0]
    }
}

function BasicPlotlyGraph() {
    const [plotData, setPlotData] = useState([new singlePlot()]);
    // const [yData, setYData] = useState([0])

    const plotJSON = {
        data: [{
            x: [1,2,3,4],
            y: [1,3,2,6],
            type: 'scatter',
            marker: {color: '#ab63fa'},
            name: 'Scatter'
        }, {
            x: [1,2,3,4],
            y: [3,2,7,4],
            type: 'line',
            marker: {color: '#19d3f3'},
            name: 'Line'
        }],
        layout: {
            plotBackground: '#f3f6fa',
            margin: {t:0, r: 0, l: 20, b: 30},
        }
    };

    return <Plot data={plotJSON} />
}

export default BasicPlotlyGraph;
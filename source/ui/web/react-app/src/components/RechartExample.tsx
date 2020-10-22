import { Button, Tooltip } from "@material-ui/core";
import React, { useState } from "react";
import { PureComponent } from "react";
import { LineChart, CartesianGrid, XAxis, YAxis, Legend, Line, Scatter, ScatterChart, ZAxis } from "recharts";

const data = [
    {
      "name": 5,
      "uv": 4000,
      "pv": 2400,
      "amt": 2400
    },
    {
      "name": 10,
      "uv": 3000,
      "pv": 1398,
      "amt": 2210
    },
    {
      "name": 15,
      "uv": 2000,
      "pv": 9800,
      "amt": 2290
    },
    {
      "name": 20,
      "uv": 2780,
      "pv": 3908,
      "amt": 2000
    },
    {
      "name": 25,
      "uv": 1890,
      "pv": 4800,
      "amt": 2181
    },
    {
      "name": 100,
      "uv": 2390,
      "pv": 3800,
      "amt": 2500
    },
    {
      "name": 200,
      "uv": 3490,
      "pv": 4300,
      "amt": 2100
    }
]

export default function RechartLineChartExample(){
    return <>
    <LineChart width={730} height={250} data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        {/* <Tooltip /> */}
        <Legend />
        <Line type="monotone" dataKey="pv" stroke="#8884d8" />
        <Line type="monotone" dataKey="uv" stroke="#82ca9d" />
    </LineChart>
    </>
}

const data01 = [{ x: 10, y: 30 }, { x: 30, y: 200 }, { x: 45, y: 100 }, { x: 50, y: 400 }, { x: 70, y: 150 }, { x: 100, y: 250 }];
const data02 = [{ x: 30, y: 20 }, { x: 50, y: 180 }, { x: 75, y: 240 }, { x: 100, y: 100 }, { x: 120, y: 190 }, {x: 300, y: 190}];

export function RechartScatterExample()  {

  const [scatterData, setScatterData] = useState({"data01": data01, "data02": data02})

  const newData = () => {
    scatterData["data01"].concat({x : 160, y : 100});
    setScatterData(scatterData);
  }

  return <>
    <Button onClick={newData}>Add data</Button>
    <ScatterChart
      width={500}
      height={400}
      margin={{
        top: 20, right: 20, bottom: 20, left: 20,
      }}
    >
      <CartesianGrid />
      <XAxis type="number" dataKey="x" name="stature" unit="cm" />
      <YAxis type="number" dataKey="y" name="weight" unit="kg" />
      <ZAxis type="number" range={[100]} />
      {/* <Tooltip cursor={{ strokeDasharray: '3 3' }} /> */}
      <Legend />
      <Scatter name="data 01" data={scatterData["data01"]} fill="#8884d8" line />
      <Scatter name="data 02" data={scatterData["data02"]} fill="#82ca9d" line />
    </ScatterChart>
  </>
}

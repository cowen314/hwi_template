import { Tooltip } from "@material-ui/core";
import React from "react";
import { LineChart, CartesianGrid, XAxis, YAxis, Legend, Line } from "recharts";

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
    //   "pv": 1398,
      "amt": 2210
    },
    {
      "name": 15,
    //   "uv": 2000,
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

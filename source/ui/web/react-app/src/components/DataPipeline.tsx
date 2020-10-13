import React, { useState, useEffect } from 'react';
import { JsxElement } from 'typescript';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import { IconButton } from '@material-ui/core';
import { SocketType } from '../custom_type_declarations/common-types';

// Goal: determine how to best pass frequently updating data/tags to React components,
// where the components need to render a variable number of tags (e.g. in a dynamic list, graph, etc) 

// Option 1: using composition
// Pass the data in as props

function ValueTable(props : {tags : any}){  // FIXME
    return <>
    <Table size="small">
        <TableHead>
        <TableRow>
            <TableCell>Value</TableCell>
        </TableRow>
        </TableHead>
        <TableBody>
        {
            // for (var key in tags) {
            //     <TableRow id="1">
            //         <TableCell>1</TableCell>
            //     </TableRow>
            // }

            // Object.entries(props.tags).forEach(([k,v]) => {
            //     <TableRow id="1">
            //         <TableCell>1</TableCell>
            //     </TableRow>
            // })

            Object.keys(props.tags).map((key) => (
                <TableRow id={key}>
                    <TableCell>{key as string}</TableCell>
                    <TableCell>{props.tags[key] as number}</TableCell>
                </TableRow>
            ))

            // Object.entries(tags).forEach(([key, val]) => (
            //     <TableRow id="1">
            //         <TableCell>1</TableCell>
            //     </TableRow>
            // )
        }
        </TableBody>
    </Table>
    </>
}

function updateBuffer() {

}

function DataBuffers(props: {socket: SocketType}, socketEventName: string, lengths: BigInteger) {
    const [bufferedData, setBufferedData] = useState({}); // dictionary(string, number[]))
    // LEFT OFF HERE: when something happens (new tags data received), we need to update the buffers
    // const newDataReceived = () => {

    // };
    useEffect(props.socket.on(socketEventName, (data: any) => {  // FIXME switch the type of `data`
        // concatenate the values in the dictionary with existing values in the buffer, removing old samples
        Object.keys(data).forEach((key) => (bufferedData as any)[key].concatenate(data[key]));  // TODO rotate out any samples beyond given length
        setBufferedData(bufferedData);
    }));
}

function Graph(props: {dataBuffers: JsxElement}) {
    // store the current values in buffers (part of this component's state)
    // when something happens, the buffers here get updated
    // don't think this can be compositional, because it actually has state
    // we _could_ pass a buffer component into this as a prop... yeah, let's do that

    // OK so I think?? I might need to use context here?
    // LEFT OFF HERE: It seems like I need to "subscribe" to rerenders of the DataBuffers... 
    return <React.Fragment>
        <Title>Today</Title>
        <ResponsiveContainer>
          <LineChart
            data={data}
            margin={{
              top: 16,
              right: 16,
              bottom: 0,
              left: 24,
            }}
          >
            <XAxis dataKey="time" stroke={theme.palette.text.secondary} />
            <YAxis stroke={theme.palette.text.secondary}>
              <Label
                angle={270}
                position="left"
                style={{
                  textAnchor: 'middle',
                  fill: theme.palette.text.primary,
                }}
              >
                Sales ($)
              </Label>
            </YAxis>
            <Line
              type="monotone"
              dataKey="amount"
              stroke={theme.palette.primary.main}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </React.Fragment>
}


export default function CompositionApproach() {
    const [tags, setTags] = useState({
        "testTag123": 123
    });
    const setRandomTags = () => {
        // var test : Record<string, number> = {"test": 1};
        var test : any = {"test": 1}; // FIXME find appropriate type
        for (var i=0; i < 5; i++) {
            test[i.toString()] = Math.random();
        }
        setTags(test);
    }
    return <>
    <IconButton onClick={setRandomTags}>Generate New Tags</IconButton>
    <ValueTable tags={tags}/>
    </>
}



// Option 2: Using context
// Grab the data with the `UseContext` hook
import React, { useState } from 'react';
import { JsxElement } from 'typescript';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import { IconButton } from '@material-ui/core';

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
                <TableRow>
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

function generateDataRows(tags: {}) {

}

export default function CompositionApproach() {
    const [tags, setTags] = useState({
        "testTag123": 123
    });
    const setRandomTags = () => {
        // var test : Record<string, number> = {"test": 1};
        var test : any = {"test": 1}; // FIXME remove `any`
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
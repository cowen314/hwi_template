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

function Tag(props : {data: number, key: string, displayKey: boolean}) {
    if (!props.displayKey){
        return <p>{props.data}</p>
    }
    return <p>{props.key} - {props.data}</p>
}

// Option 1: using composition
// Pass the data in as props

function ValueTable(props : {tags: {}}){
    return <>
    <Table size="small">
        <TableHead>
        <TableRow>
            <TableCell>Value</TableCell>
        </TableRow>
        </TableHead>
        <TableBody>
        Object.entries(tags).forEach(([key, val]) => {
            <TableRow id={key}>
                <TableCell>{val}</TableCell>
            </TableRow>
        });
        {/* {props.tags.map((tag) => (

        ))} */}
        </TableBody>
    </Table>
    </>
}

function TagCatcher() {
    const [tags, setTags] = useState({
        "testTag123": 123
    });
    const setRandomTags = () => {
        var test = {};
        for (var i=0; i > 5; i++) {
            test[i.toString()] = i;
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
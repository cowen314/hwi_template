import React, { useState, useEffect } from 'react';
import { JsxElement } from 'typescript';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import { Button, Container, IconButton, makeStyles, useTheme } from '@material-ui/core';
import { SocketType } from '../custom_type_declarations/common-types';
import { ResponsiveContainer, LineChart, XAxis, YAxis, Label, Line } from 'recharts';
import Title from '../dashboard/Title';
import io from 'socket.io-client';
// import { useStyles } from '../dashboard/Dashboard';

// Goal: determine how to best pass frequently updating data/tags to React components,
// where the components need to render a variable number of tags (e.g. in a dynamic list, graph, etc) 

// Option 1: using composition
// Pass the data in as props

const drawerWidth = 240;

export const useStyles = makeStyles((theme) => ({
    root: {
      display: 'flex',
    },
    toolbar: {
      paddingRight: 24, // keep right padding when drawer closed
    },
    toolbarIcon: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'flex-end',
      padding: '0 8px',
      ...theme.mixins.toolbar,
    },
    appBar: {
      zIndex: theme.zIndex.drawer + 1,
      transition: theme.transitions.create(['width', 'margin'], {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
      }),
    },
    appBarShift: {
      marginLeft: drawerWidth,
      width: `calc(100% - ${drawerWidth}px)`,
      transition: theme.transitions.create(['width', 'margin'], {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
      }),
    },
    menuButton: {
      marginRight: 36,
    },
    menuButtonHidden: {
      display: 'none',
    },
    title: {
      flexGrow: 1,
    },
    drawerPaper: {
      position: 'relative',
      whiteSpace: 'nowrap',
      width: drawerWidth,
      transition: theme.transitions.create('width', {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
      }),
    },
    drawerPaperClose: {
      overflowX: 'hidden',
      transition: theme.transitions.create('width', {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
      }),
      width: theme.spacing(7),
      [theme.breakpoints.up('sm')]: {
        width: theme.spacing(9),
      },
    },
    appBarSpacer: theme.mixins.toolbar,
    content: {
      backgroundColor:
        // theme.palette.mode === 'light'
        //   ? theme.palette.grey[100]
        //   : theme.palette.grey[900],
        theme.palette.grey[100],
      flexGrow: 1,
      height: '100vh',
      overflow: 'auto',
    },
    container: {
      paddingTop: theme.spacing(4),
      paddingBottom: theme.spacing(4),
    },
    paper: {
      padding: theme.spacing(2),
      display: 'flex',
      overflow: 'auto',
      flexDirection: 'column',
    },
    fixedHeight: {
      height: 240,
    },
}));

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

function BufferedSocketGraph(props: {socket: SocketType, socketEventName: string, lengths: number}) {
    // TODO move the buffering logic to another component or entity that can be reused in other places where buffering is needed
    const [bufferedData, setBufferedData] = useState({}); // dictionary(string, number[]))
    useEffect(
        () => {
            props.socket.on(props.socketEventName, (data: any) =>
            {  // FIXME switch the type of `data`
            // concatenate the values in the dictionary with existing values in the buffer, removing old samples
                setBufferedData(shuffleInBufferMultipoint(data, bufferedData, props.lengths));
            })
        }  // be sure to get the brackets correct here, the errors throw as a result of incorrect brackets can be quite confusing
    );
    return <>
    <Graph data={bufferedData}/>
    </>
}

function BufferedButtonGraph(props: {lengths: number}){
    const [bufferedData, setBufferedData] = useState({"name":"plot1"});  // dictionary(string, number[]))
    const newDataRequested = () => setBufferedData(shuffleInBufferMultipoint({"plot1":Math.random()}, bufferedData, props.lengths))
    return <>
    <Button onClick={newDataRequested}>New Data</Button>
    <Graph data={bufferedData}/>
    </>
}

function shuffleInBufferMultipoint(newData: any, bufferedData: any, bufferLength: number){  // FIXME move away from any
    Object.keys(newData).forEach((key) =>
        {
            bufferedData[key] = bufferedData[key].concat(newData[key]);
            if (bufferedData[key].length > bufferLength){
                bufferedData[key] = bufferedData[key].slice(bufferedData[key].length-bufferLength);
            }
        }
    );
    return bufferedData;
}

// LEFT OFF HERE - 
// NOt sure if Recharts is the plotting library that I should be using here. 
// Get a plotting library that works first,
// then implement all of this buffering stuff and get click driven updates working,
// then get it working with the socket 

// assumed that bufferedData is a list of 
function shuffleInBufferSinglePoint(newData: any, bufferedData: any, bufferLength: number){
    
}

// function DataBuffer(props: {socket: SocketType, socketEventName: string, lengths: BigInteger}) {

// }

function Graph(props: {data: any}) {
    const theme = useTheme();
    // store the current values in buffers (part of this component's state)
    // when something happens, the buffers here get updated
    // don't think this can be compositional, because it actually has state
    // we _could_ pass a buffer component into this as a prop... yeah, let's do that

    // OK so I think?? I might need to use context here?

    // Option 1: use context
    // I would create a context,
    // wrap the graph object in that context,
    // then implement the graph so that it pulls from the context.
    // 

    // Option 2: pass the databuffers piece of the state of the DataBuffers into this class
    // is this possible without nesting this component directly in the data buffers component?
    // could maybe get around direct nesting with generics

    return <React.Fragment>
        <Title>Today</Title>
        <ResponsiveContainer>
          <LineChart
            data={props.data}
            margin={{
              top: 16,
              right: 16,
              bottom: 0,
              left: 24,
            }}
          >
            <XAxis dataKey="time" stroke={theme.palette.text.secondary} />
            {/* <XAxis /> */}
            <YAxis stroke={theme.palette.text.secondary}>
            {/* <YAxis> */}
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
    const classes = useStyles();
    const [tags, setTags] = useState({
        "testTag123": 123
    });
    const socket = io.connect('http://localhost:5001');
    const setRandomTags = () => {
        // var test : Record<string, number> = {"test": 1};
        var test : any = {"test": 1}; // FIXME find appropriate type
        for (var i=0; i < 5; i++) {
            test[i.toString()] = Math.random();
        }
        setTags(test);
    }
    return <div className={classes.root}>
        <main className={classes.content}>
            <Container maxWidth="lg" className={classes.container}>
                <IconButton onClick={setRandomTags}>Generate New Tags</IconButton>
                <ValueTable tags={tags}/>
                <BufferedSocketGraph socket={socket} socketEventName="testEvent" lengths={10}/>
            </Container>
        </main>
    </div>
}



// Option 2: Using context
// Grab the data with the `UseContext` hook
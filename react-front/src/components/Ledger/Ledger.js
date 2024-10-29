import {Panel} from "reactflow";
import React, {useContext, useState} from "react";
import Box from "@mui/material/Box";
import {Message} from "../Message/Message";
import {UserContext} from "../contexts/UserContext";


export function Ledger({schemaName,
                       update_schema}) {
    const {username, sessionkey} = useContext(UserContext)

    const [showLedger, setShowLedger] = useState(false);
    const [messages, setMessages] = useState([]);
    const [schemaID, setSchemaID] = useState(0);
    const [userResponse, setUserResponse] = useState("")
    const [schemaIDOptions, setSchemaIDOptions] = useState([]);
    const [executionQueue, setExecutionQueue] = useState([]);
    const [currentBlockID, setCurrentBlockID] = useState(0);


    const optionsList = schemaIDOptions.map((option) => <option key={option} onClick={() => {
        setSchemaID(option);
        get_state(option);
    }}>{option}</option>);

    function make_schema_instance() {
        update_schema(username, sessionkey, schemaName);

        fetch("/sandbox/make_schema_instance/", {
            method: "GET", headers: {
                "username": username, "sessionkey": sessionkey, "schemaName": schemaName
            }
        }).then((response) => response.json()
        ).then((response) => {setSchemaID(JSON.parse(response.content)); get_schema_instances();})
    }

    function get_schema_instances() {
        return fetch("/sandbox/get_schema_instances/", {
            method: "GET", headers: {
                "username": username, "sessionkey": sessionkey, "schemaName": schemaName
            }
        }).then((response) => response.json()
        ).then((response) => setSchemaIDOptions(response.content))
    }

    function get_state() {
        fetch("/sandbox/get_state/", {
            method: "GET", headers: {
                "username": username, "sessionkey": sessionkey, "schemaName": schemaName, "schemaID": schemaID
            }
        }).then((response) => response.json()
        ).then((response) => {
            setMessages([]);
            setMessages(response.content.ledger);
            setCurrentBlockID(response.content.currentBlockID)
            setExecutionQueue(response.content.executionQueue);
        })
    }

    function execute_next() {
        fetch("/sandbox/execute_next/", {
            method: "GET", headers: {
                "username": username, "sessionkey": sessionkey, "schemaName": schemaName, "schemaID": schemaID
            }
        }).then((response) => response.json()
        ).then((response) => {setMessages([]);setMessages(response.content);
            get_state();})
    }

    function deliver_content() {
        fetch("/sandbox/deliver_content/", {
            method: "GET", headers: {
                "username": username, "sessionkey": sessionkey, "schemaName": schemaName, "schemaID": schemaID, "blockID": 1, "content": userResponse
            }
        }).then((response) => response.json()
        ).then((response) => console.log(response))
    }

    function run() {
        fetch("/sandbox/run/", {
            method: "GET", headers: {
                "username": username, "sessionkey": sessionkey, "schemaName": schemaName, "schemaID": schemaID, "blockID": 1, "content": userResponse
            }
            }

        ).then((response) => response.json()
        ).then((response) => console.log(response))
    }

    function run_to_unprepared() {
        fetch("/sandbox/run_to_unprepared/", {
                method: "GET", headers: {
                    "username": username, "sessionkey": sessionkey, "schemaName": schemaName, "schemaID": schemaID, "blockID": 1, "content": userResponse
                }
            }

        ).then((response) => response.json()
        ).then((response) => console.log(response))
    }

    function handleSend(){
        deliver_content();
        setUserResponse("");
    }

    function handleEnter(e) {
        if (e.key === "Enter") {
            handleSend()
        }
    }

    return (
        <>
            <Panel style={{position: 'absolute'}} position={'top-right'}>
                <button onClick={() => setShowLedger(!showLedger)}>Toggle Ledger</button>
            </Panel>
            {showLedger && <Panel style={{position: 'absolute', top: '30px'}} position={'top-right'}>
                <Box label="ledgerView" component="section" sx={{
                    color: 'white',
                    borderRadius: '10px',
                    padding: '5px',
                    border: '2px solid black',
                    display: 'block',
                    height: '800px',
                    width: '500px',
                    bgcolor: '#222222',
                    '&:hover': {
                        bgcolor: '#333333',
                    },
                }}>
                    <Box sx={{bgcolor: 'blue'}}>
                        <div>Current Schema:{schemaName}</div>
                        <div>Current Instance:<select value={schemaID}
                                                      onClick={() => get_schema_instances()}>{optionsList}</select>
                        </div>
                        <div>Execution Queue:{executionQueue.map((block) =>
                            <button>BLOCK#{block}</button>
                        )}</div>
                        <div>

                        </div>

                        <div label={'buttonTray'}>
                            <button onClick={() => {
                                make_schema_instance()
                            }}>MAKE SCHEMA INSTANCE
                            </button>
                            <button onClick={get_state}>REFRESH</button>
                            <button onClick={execute_next}>EXECUTE</button>
                            <button onClick={run}>RUN</button>
                            <button onClick={run_to_unprepared}>RUN TO UNPREPARED</button>
                        </div>
                    </Box>

                    <Box sx={{height: '650px', width: '500px'}} overflow={'auto'}>

                        <Box sx={{}}>{messages.map((data) => <Message data={data}/>)}
                            <div label={'bottom'}/>
                        </Box>

                    </Box>


                    <Box component="section" sx={{
                        position: 'absolute', left: '15px', bottom: '15px',
                        color: 'white',
                        borderRadius: '15px',
                        padding: '10px', display: 'block', width: '460px', bgcolor: '#555555', '&:hover': {
                            bgcolor: '#555555',
                        },
                    }}><input style={{
                        border: 'none', outline: 'none', background: 'transparent', color: 'white', width: "409px"
                    }}
                              type="text"
                              className="nodrag"
                              name="userResponse"
                              value={userResponse}
                              onKeyDown={handleEnter}
                              onChange={e => setUserResponse(e.target.value)}></input>
                        <button onClick={handleSend}>SEND</button>
                    </Box>
                </Box>
            </Panel>}
        </>)
}
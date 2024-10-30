import {Controls, useReactFlow, useStoreApi, Panel} from "reactflow";
import EditableText from "../EditableText/EditableText";
import React, {useContext, useEffect, useState} from "react";
import Box from "@mui/material/Box";

import './CustomControls.css';
import AddNodeButton from "../AddNodeButton/AddNodeButton";
import {Ledger} from "../Ledger/Ledger";
import {UserContext} from "../contexts/UserContext";
import Modal from "../Modal/Modal";
import Timer from "../Timer";

export function CustomControls({
                                   nodes,
                                   edges,
                                   position,
                                   onChange,
                                   schemaName,
                                   schemaOptions,
                                   setSchemaName,
                                   editSchemaName,
                                   setEditSchemaName,
                                   set_schema_list,
                                   send_schema,
                                   get_schema,
                                   update_schema,
                                   light_em_up,
                               }) {
    const username = useContext(UserContext);
    const [modalContent, setModalContent] = useState("We love modals here")
    const [pageView, setPageView] = useState(0);
    const {setNodes, zoomIn, zoomOut, setCenter} = useReactFlow()


    const optionsList = schemaOptions.map((option) => <option key={option} onClick={() => {
        setSchemaName(option);
        get_schema(option);
    }}>{option}</option>);

    const nextID = () => {
        // todo: once abstracted, maintain a 'free id list' that is appended on delete; n -> 1
        let targetID = 1;
        const ids = nodes.map((node) => node.id.toString());
        while (ids.includes(targetID.toString())) {
            targetID += 1;
        }
        return targetID;
    };


    function selectNode(target_node) {
        // todo: implement focus for component's children
        const x = target_node.position.x + target_node.width / 2;
        const y = target_node.position.y + target_node.height / 2;
        const zoom = 1.85;

        setCenter(x, y, {zoom, duration: 1000});

        nodes.map((node) => target_node.id === node.id ? node.selected = true : node.selected = false);
        edges.map((edge) => edge.selected = false);
        onChange(nodes, edges);
    }

    function listNodes() {
        return (nodes.map(node => node.selected ? <div>
            <button><strong>BLOCK#{node.id} : {node.data.label}</strong></button>
        </div> : <div>
            <button onClick={(e) => selectNode(node)}>BLOCK#{node.id} : {node.data.label}</button>
        </div>))
    }

    function selectEdge(target_edge) {
        // todo: implement focus for edges
        edges.map((edge) => target_edge.id === edge.id ? edge.selected = true : edge.selected = false);
        nodes.map((node) => node.selected = false);
        onChange(nodes, edges);
    }

    function listEdges() {
        return (edges.map(edge => edge.selected ? <div>
            <button><strong>EDGE#{edge.id}</strong></button>
        </div> : <div>
            <button onClick={(e) => selectEdge(edge)}>EDGE#{edge.id}</button>
        </div>))
    }


    function renderPage() {
        switch (pageView) {
            case(0):
                return <Controls position='top-left' style={{position: 'absolute', top: '30px'}} showZoom={false} showFitView={false}
                                 showInteractive={false}>
                    <Box component="section" sx={{
                        color: 'white',
                        borderRadius: '10px',
                        padding: '5px',
                        border: '2px solid black',
                        display: 'block',
                        bgcolor: '#222222',
                        '&:hover': {
                            bgcolor: '#333333',
                        },
                    }}
                    >
                        {/*<div align={'center'} style={{fontSize: '40px', fontFamily: 'sans-serif'}}>The quick brown fox jumps over the lazy dog.</div>*/}

                        <div className={"schema-control"}>
                            <div>
                                Select Schema:<select value={schemaName} onClick={() => set_schema_list()}>
                                    {optionsList}
                                </select>
                                <button onClick={update_schema}>SAVE</button>
                            </div>
                            <EditableText editing={true} name={'schema'} value={editSchemaName}
                                          setValue={setEditSchemaName}></EditableText>
                            <button onClick={() => {
                                send_schema();
                                setSchemaName(editSchemaName);
                                setEditSchemaName("");
                                set_schema_list();
                            }}>SAVE AS
                            </button>
                            {/*<button onClick={get_schema}>Load the schema! (change to on-option selection)</button>*/}

                        </div>

                        <Box>
                            Node List
                        </Box>

                        <Box maxHeight='300px' overflow={'auto'}>
                            {listNodes()}
                            <AddNodeButton nodes={nodes} setNodes={setNodes} nextID={nextID}/>
                        </Box>

                        <div>
                            Edge List
                        </div>

                        <Box maxHeight='300px' overflow={'auto'}>
                            {listEdges()}
                        </Box>


                    </Box>
                </Controls>

            case(1):
                return <Controls position='top-left' style={{position: 'absolute', top: '30px'}} showZoom={false} showFitView={false}
                                 showInteractive={false}>
                    <Box component="section" sx={{
                        borderRadius: '10px',
                        padding: '5px',
                        border: '2px solid grey', display: 'block', bgcolor: '#eeeeee', '&:hover': {
                            bgcolor: '#ffffff',
                        },
                    }}
                    >
                        Credentials <select/>
                        <form>
                            <div>NAME:<input/></div>
                            <div>API-KEY:<input/></div>
                        </form>
                    </Box>
                </Controls>

            case(2):
                return <Controls style={{position: 'absolute', top: '30px'}} showZoom={false} showFitView={false}
                                 showInteractive={false}>
                    <Box component="section" sx={{
                        border: '2px solid grey', display: 'block', bgcolor: '#eeeeee', '&:hover': {
                            bgcolor: '#ffffff',
                        },
                    }}
                    >
                        <div>
                            This is where you add / edit functions for Responders and Switches.
                        </div>
                        <div>
                            <select>
                                <option>Coming soon!</option>
                            </select>
                        </div>
                </Box>
            </Controls>

            }
            }

            return (
                <>
                    <Panel style={{position: 'absolute'}} position={'top-left'}>
                        <div>
                            <button onClick={() => setPageView(0)}>
                                Schema Overview
                            </button>

                            {/*<button onClick={() => setPageView(1)}>*/}
                            {/*    Credentials*/}
                            {/*</button>*/}

                            {/*<button onClick={() => setPageView(2)}>*/}
                            {/*    Custom Response Functions*/}
                            {/*</button>*/}
                        </div>
                    </Panel>
                    {renderPage()}
                    <Ledger schemaName={schemaName} update_schema={update_schema} nodes={nodes} selectNode={selectNode} light_em_up={light_em_up}/>
                    <Panel id={"modal-manager"} style={{position: 'absolute'}} position={'top-center'}>
                        {modalContent !== "" && <Modal onClick={() => setModalContent("")} content={modalContent}></Modal>}
                    </Panel>
                </>
            )
            }
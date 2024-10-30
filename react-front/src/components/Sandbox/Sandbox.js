import React, {useContext, useEffect, useState} from "react";
import Box from "@mui/material/Box";
import {useCallback} from 'react';
import ReactFlow, {
    MiniMap,
    Controls,
    Background,
    getIncomers,
    getOutgoers,
    getConnectedEdges,
    useNodesState,
    useEdgesState,
    addEdge,
    MarkerType, useReactFlow, Panel,
} from 'reactflow';

import 'reactflow/dist/style.css';
import customNode from "../CustomNode/CustomNode";
import customEdge from "../CustomEdge/CustomEdge";
import {CustomControls} from "../CustomControls/CustomControls";
import useWindowDimensions from "../WindowDimensions";
import {UserContext} from "../contexts/UserContext";
import Modal from "../Modal/Modal";
import {light} from "@mui/material/styles/createPalette";
import styled from "styled-components";

const nodeTypes = {
    customNode: customNode,
}

const edgeTypes = {
    customEdge: customEdge,
}

const startNode = {
    id: '0',
    position: {x: 0, y: 0},
    type: 'customNode',
    data: {blockType: 'System', label: 'START', isJoin: false, connected: true, color: '#AEC4FF'},
    className:"nodrag",
}

const defaultViewport = {x: 300, y: 200, zoom: 1.5};


export function Sandbox() {
    const {username, sessionkey} = useContext(UserContext)
    // react flow values
    const [schemaOptions, setSchemaOptions] = useState([]);
    const [schemaName, setSchemaName] = useState("default");
    const [editSchemaName, setEditSchemaName] = useState("");
    const [nodes, setNodes, onNodesChange] = useNodesState([startNode]);
    const [edges, setEdges, onEdgesChange] = useEdgesState([]);

    const onConnect = useCallback((params) => {
        setEdges((eds) => {
        params.type = 'customEdge';
        params.animated = false;
        params.data = {dependent: false};
        // params.zIndex = 5;
        params.id = `${params.source}->${params.target}`;
        return addEdge(params, eds);
        });
    }, [setEdges]);

    const onChange = useCallback((nodes, edges) => {


        setNodes(nodes.map((node) => node));
        setEdges(edges.map((edge) => edge));
    }, []);

    const onNodesDelete = useCallback((deleted) => {
        setEdges(deleted.reduce((acc, node) => {
            const incomers = getIncomers(node, nodes, edges);
            const outgoers = getOutgoers(node, nodes, edges);
            const connectedEdges = getConnectedEdges([node], edges);

            const remainingEdges = acc.filter((edge) => !connectedEdges.includes(edge),);

            const createdEdges = incomers.flatMap(({id: source}) => outgoers.map(({id: target}) => ({
                id: `e${source}-${target}`, type: 'customEdge', data: {dependent: false}, source, target,
            })),);

            return [...remainingEdges, ...createdEdges];
        }, edges),);
    }, [nodes, edges],);

    function set_schema(schema_obj) {
        setNodes(schema_obj.nodes);
        setEdges(schema_obj.edges);
    }

    function set_schema_list() {
        return fetch('/sandbox/schema_list/', {
            method: "GET", headers: {"username": username, "sessionkey": sessionkey}
        }).then(response => response.json()).then(response => {
            setSchemaOptions(response.content);
        })
    }

    function get_schema(aSchema) {
        fetch('/sandbox/schema/', {
            method: "GET", headers: {"username": username, "sessionkey": sessionkey, "schemaName": aSchema}
        }).then(response => response.json()).then(response => set_schema(JSON.parse(response.content)))
    }

    function send_schema() {
        fetch('/sandbox/schema/', {
            method: "PUT",
            headers: {"username": username, "sessionkey": sessionkey, "schemaName": editSchemaName},
            body: JSON.stringify({nodes: nodes, edges: edges})
        })
    }

    function update_schema() {
        fetch('/sandbox/schema/', {
            method: "POST",
            headers: {"username": username, "sessionkey": sessionkey, "schemaName": schemaName},
            body: JSON.stringify({nodes: nodes, edges: edges})
        })
    }

    function get_connected_nodes() {
        // creates a list of nodes that have a connection to start
        let visited = [];
        let queue = ["0"];

        while(queue.length > 0) {
            const current = queue.shift();
            if (!visited.includes(current)) {
                visited = [...visited, current]
                // add targets where current is source
                const outgoing_flow = edges.filter(edge => (edge.source === current)  & !edge.data.dependent);
                const incoming_dependencies = edges.filter(edge => (edge.target === current) & edge.data.dependent);
                // filter to remove visited nodes
                const next_targets = outgoing_flow.filter(edge => !visited.includes(edge.target))
                const next_depends = incoming_dependencies.filter(edge => !visited.includes(edge.source))
                // queue everything in next_targets
                queue = [...queue, ...next_targets.map(edge => edge.target)];
                queue = [...queue, ...next_depends.map(edge => edge.source)];
            }
        }

        return visited;
    }


    function light_em_up() {
        setNodes(nodes.map((node) =>
            get_connected_nodes().includes(node.id)
                ? {...node, data : {...node.data, connected: true}}
                : {...node, data : {...node.data, connected: false}}));
    }


    return (
        <div align={'left'}>
            {/*<button onClick={light_em_up}>LIGHT EM UP</button>*/}
            <Box component="section" sx={{
                border: '2px solid black',
                display: 'block',
                // width: '1080px',
                height: '1080px',
                bgcolor: '#eeeeee',
                '&:hover': {
                    bgcolor: '#ffffff',
                },
            }}
            >
                <ReactFlow
                    nodes={nodes}
                    nodeTypes={nodeTypes}
                    edges={edges}
                    edgeTypes={edgeTypes}
                    onNodesDelete={onNodesDelete}
                    onNodesChange={onNodesChange}
                    onEdgesChange={onEdgesChange}
                    onConnect={onConnect}
                    defaultViewport={defaultViewport}
                    style={{background: "#111111"}}
                    snapToGrid={true}
                    snapGrid={[10, 10]}
                >
                    {/*<MiniMap/>*/}
                    {/*<Controls/>*/}
                    <CustomControls
                                    nodes={nodes}
                                    edges={edges}
                                    position={'top-left'}
                                    onChange={onChange}
                                    schemaName={schemaName}
                                    setSchemaName={setSchemaName}
                                    editSchemaName={editSchemaName}
                                    setEditSchemaName={setEditSchemaName}
                                    set_schema_list={set_schema_list}
                                    schemaOptions={schemaOptions}
                                    get_schema={get_schema}
                                    send_schema={send_schema}
                                    update_schema={update_schema}
                                    light_em_up={light_em_up}
                    ></CustomControls>
                    <Background/>
                </ReactFlow>


            </Box>

        </div>);
}
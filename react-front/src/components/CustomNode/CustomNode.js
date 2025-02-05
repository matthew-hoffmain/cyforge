import React, {useEffect, useState, useRef} from 'react';
import ReactFlow, {
    Handle, NodeToolbar, Position, useNodesState, useReactFlow, NodeResizer
} from 'reactflow';
import EditableText from "../EditableText/EditableText";

import './CustomNode.css';
import EditableOption from "../EditableOption/EditableOption";
import Box from "@mui/material/Box";
import styled from 'styled-components';

const blockTypes = ['System', 'Responder', 'Switch', 'Component', 'Test']


function get_color(data) {
    const this_alpha = data.connected ? "FF" : "AA"

    return data.color + this_alpha;
}

function get_glow(data) {
    if (data.connected) {
        return "0 0 20px " + get_color(data);
    }
    else {
        return ''
    }
}


export default function CustomNode({id, data, isConnectable}) {

    const {addNodes, setNodes} = useReactFlow();

    const [editing, setEditing] = useState(data.editing);
    const [blockName, setBlockName] = useState(data.label);
    const [isJoin, setIsJoin] = useState(data.isJoin);
    const [connected, setConnected] = useState(data.connected);
    const [color, setColor] = useState(data.color);

    const [blockType, setBlockType] = useState(data.blockType);
    const [subtype, setSubtype] = useState(data.subtype);
    // responder values
    const [input, setInput] = useState(data.input);
    const [output, setOutput] = useState(data.output);
    // responder-echo
    const [content, setContent] = useState(data.content);
    // responder-model
    const [credentials, setCredentials] = useState(data.credentials);

    function duplicateNode() {
        addNodes({
            id: '10',
            position: {x: 0, y: 0},
            type: 'customNode',
            data: {
                id: '10',

                editing: editing,
                label: blockName,
                isJoin: isJoin,
                connected: connected,
                color: color,

                // todo: abstract so that blocktype is a class or something fr
                blockType: blockType,
                subtype: subtype,
                // responder values
                input: input,
                output: output,
                // responder-echo
                content: content,
                // responder-model
                credentials: credentials,
            }
        });
    }

    function handleSubmit(e) {
        e.preventDefault();
        console.log('Form submission not implemented yet! Nice job hitting enter though!');
    }

    function renderBlockType() {
        const name = 'cool';
        switch (blockType) {
            case 'Responder':
                return (
                    <>
                        <div>
                            Response Function:<strong>
                            <EditableOption editing={editing} name='Response Function' options={['Echo', 'User Text Input', 'User Audio Input', 'Model']}
                                            setValue={setSubtype} value={subtype}>
                            </EditableOption></strong>
                        </div>
                        {subtype === "Model" ?
                            <>
                                <div>
                                    Model Input:<strong>
                                    <EditableOption editing={editing} name='Model Input' options={['Text', 'Audio', 'Image']}
                                                    setValue={setInput} value={input}>
                                    </EditableOption></strong>
                                </div>
                                <div>
                                    Model Output:<strong>
                                    <EditableOption editing={editing} name='Model Output' options={['Text', 'Audio', 'Image']}
                                                    setValue={setOutput} value={output}>
                                    </EditableOption></strong>
                                </div>
                                <div>
                                    API Credentials:<strong>
                                    <EditableOption editing={editing} name='API Credentials' options={['ADMIN openai']}
                                                    setValue={setCredentials} value={credentials}>
                                    </EditableOption></strong>
                                </div>
                            </> : <></>}
                        {subtype === "Echo" ?
                            <>
                                <div>
                                    Prompt:<strong>
                                    <EditableText editing={editing} name='content'
                                                    setValue={setContent} value={content}>
                                    </EditableText></strong>
                                </div>
                            </> : <></>}
                    </>);
            case 'Switch':
                return (
                    <>
                        <div>
                            Switch Function:<strong>
                            <EditableOption editing={editing} name='Switch Function' options={['Audio-In Enabled', 'Audio-Out Enabled']}
                                            setValue={setSubtype} value={subtype}>
                            </EditableOption></strong>
                        </div>
                    </>);
            case 'Component':
                return (
                    <>
                        <Box component="section" sx={{
                            border: '2px solid black', // display: 'inline-flex',
                            display: 'block',
                            height: '300px',
                            width: '400px',
                            bgcolor: 'green', '&:hover': {
                                bgcolor: 'green',
                            },
                        }}
                        >
                            <div>
                                <EditableOption editing={true} value={name} options={['defaultSubschema', 'orAnother']}/></div>
                        </Box>
                    </>);
            case 'Test':
                return (
                    <>
                        <div>
                            Test Function:<strong>
                            <EditableOption editing={editing} name='Test Function' options={['Numbah 1', 'Numbah 2']}
                                            setValue={setSubtype} value={subtype}>
                            </EditableOption></strong>
                        </div>
                    </>);
            default:
                return;
        }
    }

    function colorChange(event) {
        setColor(event.target.value);
    }

    function updateNode(node) {

        node.data.editing = editing;
        node.data.label = blockName;
        node.data.isJoin = isJoin;
        node.data.color = color;

        // todo: abstract so that blocktype is a class or something fr
        node.data.blockType = blockType;
        node.data.subtype = subtype;
        // responder values
        node.data.input = input;
        node.data.output = output;
        // responder-echo
        node.data.content = content;
        // responder-model
        node.data.credentials = credentials;

        // ALL VALUES THAT ARE HANDLED EXTERNALLY
        setConnected(node.data.connected);

        return node;
    };

    // todo: change it so someone calls and updated ALL nodes, right now each node searches the list for itself to update...n^2 -> n
    useEffect(() => {
        setNodes((nodes) => nodes.map((node) => node.id === id ? updateNode(node) : node));

    })

    return (
        <div style={{
            fontSize: '12px',
            background: get_color(data),
            border: '2px solid #444',
            borderRadius: '5px',
            textAlign: 'left',
            padding: '5px',
            boxShadow: get_glow(data)}}>

            {editing && <NodeResizer minWidth={200} minHeight={200}/>}
            <Handle
                className={'customHandle'}
                type="target"
                position={Position.Top}
                id="a"
                style={{top: -5, background: '#000'}}
                onConnect={(params) => console.log('handle onConnect', params)}
                isConnectable={isConnectable}
            />
            <div>
                BlockID:<strong>{id}</strong>
            </div>

            <div>
                BlockName:<strong>
                <EditableText editing={editing} name='blockName' value={blockName}
                              setValue={setBlockName}></EditableText></strong>
            </div>


            <div>
            </div>

            <div>
                Join:<input type="checkbox"
                            checked={isJoin}
                            onChange={e => setIsJoin(e.target.checked)}
                            disabled={!editing}


            />
                {editing && <input
                    className="nodrag"
                    type="color"
                    onChange={colorChange}
                    defaultValue={color}
                />}
            </div>
            <div>
                <>BlockType:<strong>
                    <EditableOption editing={editing} name='blockType' options={blockTypes}
                                    setValue={setBlockType} value={blockType}>

                    </EditableOption></strong>
                    {renderBlockType()}</>

            </div>


                <Handle
                    className={'customHandle'}
                    type="source"
                    position={Position.Bottom}
                    id="b"
                    isConnectable={isConnectable}
                />


                <NodeToolbar
                    isVisible={data.forceToolbarVisible || undefined}
                    position={Position.Left}
                >
                    {!editing ? <div>
                        <div>
                            <button onClick={() => {
                                setEditing(!editing)
                            }}>Edit
                            </button>
                        </div>
                        <div>
                            <button onClick={duplicateNode}>Duplicate</button>
                        </div>
                        <div>
                            <button>Delete</button>
                        </div>
                    </div> : <div>
                        <div>
                            <button type="submit" onClick={() => {
                                setEditing(!editing)
                            }}>Done
                            </button>
                        </div>
                    </div>}

                </NodeToolbar>
        </div>
);
};
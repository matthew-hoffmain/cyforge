import React, {useState} from "react";

export default function AddNodeButton({nodes, setNodes, nextID}) {

    function addNode(data) {
        // todo: abstract function, add ability to copy nodes by passing in data
        const targetID = nextID().toString();

        const newNode = {
            id: targetID,
            position: {x: 0, y: 0},
            type: 'customNode',
            data: {
                id: targetID,

                editing: false,
                label: "NewNode",
                isJoin: false,
                connected: false,
                color: '#FFFFFF',

                // todo: abstract so that blocktype is a class or something fr
                blockType: "System",
                subtype: "Echo",
                // responder values
                input: "Text",
                output: "Text",
                // responder-echo
                content: "",
                // responder-model
                credentials: "ADMIN openai",
            }
        }
        const newNodes = nodes.concat(newNode);

        setNodes(newNodes);
    }

    return (<button onClick={addNode}>+ADD NODE</button>)
}
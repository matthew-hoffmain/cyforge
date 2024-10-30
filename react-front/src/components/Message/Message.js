
import React, {useState} from "react";
import Box from "@mui/material/Box";
import {useReactFlow} from "reactflow";

export function Message({data, node, selectNode}) {
    const message_id = useState(data.message_id);
    const block_id = useState(data.block_id);
    const timestamp = useState(data.timestamp);
    const message_type = useState(data.message_type);
    const content = useState(data.content);
    const groups = useState(data.groups);

    return (
        <Box sx={{padding: '10px'}}>
        <Box component="section" sx={{
        color: 'black',
        borderRadius: '15px',
        boxShadow: "0 0 5px " + `${node.data.color}`,
        padding: '10px', display: 'block', width:'450px', bgcolor: `${node.data.color}`, '&:hover': {
            bgcolor: `${node.data.color}`,
        },
    }}><strong><button onClick={() => selectNode(node)}>BLOCK#{block_id} : {node.data.label}</button></strong>
            <div>{content}</div>
    </Box></Box>);

}
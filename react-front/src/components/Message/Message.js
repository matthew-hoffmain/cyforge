
import React, {useState} from "react";
import Box from "@mui/material/Box";
import {useReactFlow} from "reactflow";

export function Message({data}) {
    const message_id = useState(data.message_id);
    const block_id = useState(data.block_id);
    const timestamp = useState(data.timestamp);
    const message_type = useState(data.message_type);
    const content = useState(data.content);
    const groups = useState(data.groups);


    return (
        <Box sx={{padding: '5px'}}>
        <Box component="section" sx={{
        color: 'white',
        borderRadius: '15px',
        padding: '10px', display: 'block', width:'350px', bgcolor: '#444444', '&:hover': {
            bgcolor: '#444444',
        },
    }}><strong><button>BLOCK#{block_id}</button></strong>
            <p>{content}</p>
    </Box></Box>);

}
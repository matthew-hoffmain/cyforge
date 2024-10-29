import { useState } from 'react';
import { createPortal } from 'react-dom';
import Box from "@mui/material/Box";

export default function Modal({ onClick, content }) {

    return (
        <Box className="modal" sx={{
            align: 'center',
                color: 'black',
            borderRadius: '200px',
            padding: '10px', display: 'block',
            bgcolor: '#eee', '&:hover': {
                    bgcolor: '#eee',}}}>
            <div>{content}{"   "}
                <button onClick={onClick}>Close</button>
            </div>
        </Box>
    );
}
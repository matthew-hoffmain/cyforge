import Box from "@mui/material/Box";
import React, {useContext} from "react";
import {UserContext} from "../contexts/UserContext";

export function NavBar() {

    const {username, setSessionkey} = useContext(UserContext)

    function signOut() {
        setSessionkey(0);
    }

    return (<Box className="toolbar" component="section" sx={{
        bgcolor: '#ffffff', p: .5, '&:hover': {
            bgcolor: '#ffffff',
        },
    }}>
        <Box className="left-toolbar"
             component="section"
             sx={{
                 display: 'inline-block', height: '25px', width: '33.333%', bgcolor: 'white'
             }}>
            Welcome {username}
        </Box>
        <Box className="middle-toolbar"
             component="section"
             sx={{
                 display: 'inline-block', height: '25px', width: '33.333%', bgcolor: 'white'
             }}>
            <div align={"center"}>
                HOFFMAIN - "Make what works for you."
            </div>
        </Box>
        <Box className="right-toolbar"
             align={'center'}
             component="section"
             sx={{
                 display: 'inline-block', height: '25px', width: '33.333%', bgcolor: 'white'
             }}>
            <div align={'right'}>
                <button>TEST 1</button>
                <button>TEST 2</button>
                <button onClick={signOut}> SIGN OUT</button>
            </div>
        </Box>
    </Box>)
}
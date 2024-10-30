import Box from "@mui/material/Box";
import React, {useContext} from "react";
import {UserContext} from "../contexts/UserContext";

export function NavBar() {

    const {username, setSessionkey} = useContext(UserContext)

    function signOut() {
        setSessionkey(0);
    }

    return (<Box className="toolbar" component="section" sx={{
        color: 'white',
        padding: '5px',
        display: 'block',
        bgcolor: '#222222',
        '&:hover': {
            bgcolor: '#333333',
        },
    }}>
        <Box className="left-toolbar"
             component="section"
             sx={{
                 display: 'inline-block', height: '25px', width: '33.333%',
             }}>
            Welcome {username}
        </Box>
        <Box className="middle-toolbar"
             component="section"
             sx={{
                 display: 'inline-block', height: '25px', width: '33.333%',
             }}>
            <div align={"center"}>
                <strong>CYFORGE</strong>
            </div>
        </Box>
        <Box className="right-toolbar"
             align={'center'}
             component="section"
             sx={{
                 display: 'inline-block', height: '25px', width: '33.333%',
             }}>
            <div align={'right'}>
                {/*<button>TEST 1</button>*/}
                {/*<button>TEST 2</button>*/}
                <button onClick={signOut}> SIGN OUT</button>
            </div>
        </Box>
    </Box>)
}
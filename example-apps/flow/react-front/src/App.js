import React, {useState, useEffect} from 'react';

import Cookies from 'universal-cookie';
import {SignInPage} from './components/SignInPage/SignInPage';
import {NavBar} from './components/NavBar/NavBar';
import {LoginBox} from './components/LoginBox/LoginBox';
import {RegistrationBox} from './components/RegistrationBox/RegistrationBox';
import {Sandbox} from './components/Sandbox/Sandbox';
import useWindowDimensions, {WindowDimensions} from './components/WindowDimensions';
import {Button} from "@mui/material";
import Box from "@mui/material/Box";
import {UserContext} from "./components/contexts/UserContext";
import {Panel} from "reactflow";
import Modal from "./components/Modal/Modal";


export default function App() {
    const loginCookie = new Cookies();
    const {height, width} = useWindowDimensions();
    const [username, setUsername] = React.useState(loginCookie.get('username') ? loginCookie.get('username') : "");
    const [sessionkey, setSessionkey] = React.useState(loginCookie.get('sessionkey') ? loginCookie.get('sessionkey') : 0);
    const [modalContent, setModalContent] = useState("We love modals here")


    useEffect(() => {
        fetch("/auth/check_session/", {
            method: "GET", headers: {
                "username": username, "sessionkey": sessionkey
            }
        }).then(response => response.json()).then(response => {
            if (response.content === true) {
                loginCookie.set('username', username);
                loginCookie.set('sessionkey', sessionkey);
            } else {
                setUsername('');
                loginCookie.set('username', '');
                if (!(sessionkey < 0)) {
                    setSessionkey(0);
                }
                loginCookie.set('sessionkey', sessionkey);
            }
        })
    })



    return (
    <UserContext.Provider value={{username, setUsername, sessionkey, setSessionkey}}>

        <body>
            <div id={"identity"}
                 sessionkey={sessionkey}/>

            <Box id={"root"}

                 sx={{
                     display: 'block',
                     width: width, height: height, bgcolor: 'purple'
                 }}>


                {sessionkey <= 0 && <><SignInPage/></>}

                {!(sessionkey <= 0) && <>
                    <NavBar/>
                    <Sandbox/>
                </>}
            </Box>
        </body>

    </UserContext.Provider>)


}

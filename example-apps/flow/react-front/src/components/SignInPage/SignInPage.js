import React, {useContext, useEffect} from "react";
import Box from '@mui/material/Box';
import {LoginBox} from "../LoginBox/LoginBox";
import {RegistrationBox} from "../RegistrationBox/RegistrationBox";
import {UserContext} from "../contexts/UserContext";

export function SignInPage() {

    const {setUsername, sessionkey, setSessionkey} = useContext(UserContext)

    return (
        <div>
            {sessionkey<=0 && <LoginBox setUsername={setUsername}
                                              setSessionkey={setSessionkey}/>}
            {sessionkey<=0 && <RegistrationBox keychanger={setSessionkey}/>}
            {sessionkey===-1 && "Incorrect username or password"}
            {sessionkey===-2 && "Username is already taken"}
            {sessionkey===-3 && "Passwords do not match"}
            {sessionkey===-4 && "Username is invalid length"}
            {sessionkey===-5 && "Username contains invalid characters"}
            {sessionkey===-6 && "Password is invalid"}
            {sessionkey===1 && "Password is invalid"}
        </div>
    )
}
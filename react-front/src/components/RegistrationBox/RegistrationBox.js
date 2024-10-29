import React, {useEffect} from "react";
import Box from '@mui/material/Box';


export function RegistrationBox(props) {
    const [username, setUsername] = React.useState("");
    const [password, setPassword] = React.useState("");
    const [confirmPassword, setConfirmPassword] = React.useState("");


    function handleSend() {
        fetch('/auth/add_user/', {
            method: "GET", headers: {
                "username": username, "password": password, "confirmPassword": confirmPassword,
            }
        }).then(response => response.json()).then(response => {
            console.log(response.content);
            props.keychanger(response.content);
        })
        setUsername("");
        setPassword("");
        setConfirmPassword("");
    }

    function handleEnter(e) {
        if (e.key === "Enter") {
            handleSend()
        }
    }

    return (<Box component="section" sx={{
        width: 300, border: '2px solid black', p: 1, bgcolor: '#eeeeee', '&:hover': {
            bgcolor: '#dddddd',
        },
    }}
    >
        Usernames must be between 2 and 15 alphanumeric characters.
        Passwords must be at least 6 characters.
        <div align={'center'}>
            <label>
                Username: <input type="text"
                                 value={username}
                                 onKeyDown={e => handleEnter(e)}
                                 onChange={e => setUsername(e.target.value)}/>
            </label>
        </div>
        <div align={'center'}>
            <label>
                Password: <input type="password"
                                 value={password}
                                 onKeyDown={e => handleEnter(e)}
                                 onChange={e => setPassword(e.target.value)}/>
            </label>
        </div>
        <div align={'center'}>
            <label>
                Confirm Password: <input type="password"
                                         value={confirmPassword}
                                         onKeyDown={e => handleEnter(e)}
                                         onChange={e => setConfirmPassword(e.target.value)}/>
            </label>
        </div>


        <div align={'center'}>
            <button
                type={"submit"}
                onClick={handleSend}
            >
                REGISTER
            </button>
        </div>

    </Box>)
}
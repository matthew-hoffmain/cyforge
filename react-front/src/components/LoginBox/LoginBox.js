import React, {useEffect} from "react";
import Box from '@mui/material/Box';


export function LoginBox(props) {
    const [username, setUsername] = React.useState("");
    const [password, setPassword] = React.useState("");


    function handleSend(){
        fetch('/auth/login/', {
                method: "GET",
                headers: {
                    "username": username,
                    "password": password
                }
            }
        ).then(
            response => response.json()
        ).then(
            response => {
                console.log(response.content);
                props.setSessionkey(response.content);
                if (!(response.content <= 0)) {
                    props.setUsername(username);
                }
            }
        )
        setUsername("");
        setPassword("");
    }

    function handleEnter(e) {
        if (e.key === "Enter") {
            handleSend()
        }
    }

    return (
        <Box component="section" sx={{
            width: 300,
            border: '2px solid black',
            p: 1,
            bgcolor: '#eeeeee',
            '&:hover': {
                bgcolor: '#dddddd',
            },
        }}
        >
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
                <button
                    type={"submit"}
                    onClick={handleSend}
                >
                    LOGIN
                </button>
            </div>

        </Box>
    )
}
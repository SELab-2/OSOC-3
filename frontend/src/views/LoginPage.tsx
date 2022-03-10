import React from "react";
import { useNavigate } from 'react-router-dom'

function LoginPage() {
    const navigate = useNavigate();
    return(
        <div style={{
            display: "flex",
            justifyContent: 'center',
            alignItems: 'center',
            height: '90vh'
        }}>
            <div>
                <h1>Hi!</h1>
                <h3>Welcome to the open Summer of Code selections app.</h3>
                <h3>After you've logged in with your account, we'll enable</h3>
                <h3>your account so you can get started. A admin</h3>
                <h3>will verify you as quick as possible</h3>
                <button onClick={() => navigate("/register")}>Register</button>
            </div>
        </div>
    )
}

export default LoginPage
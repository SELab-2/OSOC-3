import React from "react";
import LogInButtons from "../components/LogInButtons";

function LoginPage() {
    return(
        <div style={{
            display: "flex",
            justifyContent: 'center',
            alignItems: 'center',
            height: '90vh'
        }}>
            <div>
                <div className="welcome-text">
                    <h1 style={{marginBottom:'40px'}}>Hi!</h1>
                    <h3>Welcome to the open Summer of Code selections app.</h3>
                    <h3>After you've logged in with your account, we'll enable</h3>
                    <h3>your account so you can get started. A admin</h3>
                    <h3>will verify you as quick as possible</h3>
                </div>
                <LogInButtons/>
            </div>
        </div>
    )
}

export default LoginPage
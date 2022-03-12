import React from "react";
import { useNavigate } from 'react-router-dom'
import "../css-files/LogInButtons.css";

function LogInButtons() {
    const navigate = useNavigate();
    return(
        <div className="login-buttons">
            <div>
                <div className="email-login">
                    <button onClick={() => navigate("/register")} className="login-button">
                        <span>Log in with email</span>
                    </button>
                </div>
                <div className="google-login">
                    <button onClick={() => navigate("/register")} className="login-button">
                        <span>Log in with Google</span>
                    </button>
                </div>
                <div className="github-login">
                    <button onClick={() => navigate("/register")} className="login-button">
                        <span>Log in with Github</span>
                    </button>
                </div>
            </div>
        </div>
    )
}

export default LogInButtons
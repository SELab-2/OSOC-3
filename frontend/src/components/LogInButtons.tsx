import React from "react";
import { useNavigate } from 'react-router-dom'
import "../css-files/LogInButtons.css";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

function LogInButtons() {
    const navigate = useNavigate();
    return(
        <div className="login-buttons">
            <div>
                <div className="email-login">
                    <button onClick={() => navigate("/register")} className="login-button">
                        <div className="login-button-content">
                            <FontAwesomeIcon icon="envelope" className="mail-icon"/>
                            <span>Log in with email</span>
                        </div>
                    </button>
                </div>
                <div className="google-login">
                    <button onClick={() => navigate("/register")} className="login-button">
                        <div className="login-button-content">
                            <FontAwesomeIcon icon="envelope" className="google-icon"/>
                            <span>Log in with Google</span>
                        </div>
                    </button>
                </div>
                <div className="github-login">
                    <button onClick={() => navigate("/register")} className="login-button">
                        <div className="login-button-content">
                            <FontAwesomeIcon icon="envelope" className="github-icon"/>
                            <span>Log in with Github</span>
                        </div>
                    </button>
                </div>
            </div>
        </div>
    )
}

export default LogInButtons
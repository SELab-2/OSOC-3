import React from "react";
import OSOCLetters from "../components/OSOCLetters";

import {
    GoogleLoginButton,
    GithubLoginButton,
  } from "react-social-login-buttons";

function LoginPage() {
    return(
        <div>
            <OSOCLetters/>
            <div className="login-page-content-container">
                <div className="welcome-text">
                    <h1 style={{marginBottom:'40px'}}>Hi!</h1>
                    <h3>Welcome to the open Summer of Code selections app. After you've logged in with your account, we'll enable your account so you can get started. An admin will verify you as quick as possible</h3>
                </div>
                <div className="login">
                    <div className="socials-container">
                        <div className="socials">
                            <div className="google-login-container">
                                <GoogleLoginButton/>
                            </div>
                            <GithubLoginButton/>
                        </div>
                    </div>
                    <div className="border-right"/>

                    <div className="register-form-input-fields">
                        <div>
                            <input type="email" name="email" placeholder="Email"/>
                        </div>
                        <div>
                            <input type="password" name="password" placeholder="Password"/>
                        </div>
                        <div className="no-account">
                            Don't have an account? Ask an admin for an invite link
                        </div>
                        <div>
                            <button className="register-button">Log In</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default LoginPage
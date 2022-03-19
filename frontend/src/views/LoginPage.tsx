import React from "react";
import logoO1 from "../images/letters/osoc_orange_o.svg"
import logoS from "../images/letters/osoc_s.svg"
import logoO2 from "../images/letters/osoc_red_o.svg"
import logoC from "../images/letters/osoc_c.svg"
import { Link } from "react-router-dom";

import {
    FacebookLoginButton,
    GoogleLoginButton,
    GithubLoginButton,
  } from "react-social-login-buttons";

function LoginPage() {
    return(
        <div>
            <img src={logoO1} alt="logoO1" className="osoc-logo-O1"/>
            <img src={logoS} alt="logoS" className="osoc-logo-S"/>
            <img src={logoO2} alt="logoO2" className="osoc-logo-O2"/>
            <img src={logoC} alt="logoC" className="osoc-logo-C"/>
            <div className="login-page-content-container">
                <div>
                    <h1 style={{marginBottom:'40px'}}>Hi!</h1>
                    <h3>Welcome to the open Summer of Code selections app. After you've logged in with your account, we'll enable your account so you can get started. An admin will verify you as quick as possible</h3>
                </div>
                <h2 style={{marginBottom:'40px', marginTop:'40px'}}>Log in</h2>
                <div className="login">
                    <div className="socials">
                        <FacebookLoginButton/>
                        <GoogleLoginButton/>
                        <GithubLoginButton/>
        
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
                            <Link to="/signup">
                                Don't have an account? Click here to sign up.
                            </Link>
                        </div>
                        <div className="remember-and-reset">
                            <input type="checkbox" id="checkbox"/>
                            <label htmlFor="checkbox">Remember me</label>

                            <Link to="/home">Reset Password</Link>
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
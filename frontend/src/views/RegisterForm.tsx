import React from "react";
import OSOCLetters from "../components/OSOCLetters";
import RegisterButton from "../components/registerFormComponents/RegisterButton";

import {
    GoogleLoginButton,
    GithubLoginButton,
  } from "react-social-login-buttons";

function RegisterForm() {
    return(
        <div>
            <OSOCLetters/>
            <div className="register-form-content-container">
                <h1 style={{marginBottom:'15px'}}>Create an account</h1>
                <div style={{marginBottom:'15px', color: "grey"}}>Sign up with your social media account or email address</div>
                <div className="socials-container-register">
                        <div className="socials-register">
                            <GoogleLoginButton text="Register with Google"/>
                            <GithubLoginButton text="Register with GitHub"/>
                        </div>
                </div>

                <h2 style={{margin:'15px'}}>or</h2>
                
                <div className="register-form-input-fields">
                    <div>
                        <input type="email" name="email" placeholder="Email"/>
                    </div>
                    <div>
                        <input type="text" name="name" placeholder="Name"/>
                    </div>
                    <div>
                        <input type="password" name="password" placeholder="Password"/>
                    </div>
                    <div>
                        <input type="password" name="confirm_password" placeholder="Confirm Password"/>
                    </div>
                </div>
                <RegisterButton/>
            </div>
        </div>
    )
}

export default RegisterForm
import React from "react";
import LogInButtons from "../components/LogInButtons";
import logoO1 from "../images/letters/osoc_orange_o.svg"
import logoS from "../images/letters/osoc_s.svg"
import logoO2 from "../images/letters/osoc_red_o.svg"
import logoC from "../images/letters/osoc_c.svg"
function LoginPage() {
    return(
        <div className="login-page-container">
            <img src={logoO1} alt="logoO1" className="osoc-logo-O1"/>
            <img src={logoS} alt="logoS" className="osoc-logo-S"/>
            <img src={logoO2} alt="logoO2" className="osoc-logo-O2"/>
            <img src={logoC} alt="logoC" className="osoc-logo-C"/>
            <div className="login-page-content-container">
                <div>
                    <h1 style={{marginBottom:'40px'}}>Hi!</h1>
                    <h3>Welcome to the open Summer of Code selections app. After you've logged in with your account, we'll enable your account so you can get started. An admin will verify you as quick as possible</h3>
                </div>
                <LogInButtons/>
            </div>
        </div>
    )
}

export default LoginPage
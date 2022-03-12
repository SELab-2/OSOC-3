import React from "react";
import logoO1 from "../images/letters/osoc_orange_o.svg";
import logoS from "../images/letters/osoc_s.svg";
import logoO2 from "../images/letters/osoc_red_o.svg";
import logoC from "../images/letters/osoc_c.svg";
import RegisterButton from "../components/registerFormComponents/RegisterButton";

function RegisterForm() {
    return(
        <div>
            <img src={logoO1} alt="logoO1" className="osoc-logo-O1"/>
            <img src={logoS} alt="logoS" className="osoc-logo-S"/>
            <img src={logoO2} alt="logoO2" className="osoc-logo-O2"/>
            <img src={logoC} alt="logoC" className="osoc-logo-C"/>
            <div className="register-form-content-container">
                <div className="register-form-input-fields">
                    <span>Email:</span>
                    <div>
                        <input type="email" name="email" placeholder="example@hotmail.com"/>
                    </div>
                    <span>Password:</span>
                    <div>
                        <input type="password" name="email" placeholder="password"/>
                    </div>
                    <span>Confirm Password:</span>
                    <div>
                        <input type="password" name="email" placeholder="password"/>
                    </div>
                </div>
                <RegisterButton/>
            </div>
        </div>
    )
}

export default RegisterForm
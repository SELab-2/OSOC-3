import React from "react";
import OSOCLetters from "../components/OSOCLetters";

import RegisterButton from "../components/registerFormComponents/RegisterButton";

function RegisterForm() {
    return(
        <div>
            <OSOCLetters/>
            <div className="register-form-content-container">
                <h1>Create an account</h1>
                
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
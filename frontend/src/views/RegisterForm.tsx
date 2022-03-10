import React from "react";
import {useNavigate} from "react-router-dom";

function RegisterForm() {
    const navigate = useNavigate()
    return(
        <div>
            <label>
                Email:
                <input type="email" name="email" />
            </label>
            <button onClick={() => navigate("/students")}>Register</button>
        </div>
    )
}

export default RegisterForm
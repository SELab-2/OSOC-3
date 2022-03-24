import React from "react";
import { useNavigate } from "react-router-dom";

function RegisterButton() {
    const navigate = useNavigate();
    return (
        <div>
            <button onClick={() => navigate("/students")} className="register-button">
                Register
            </button>
        </div>
    );
}

export default RegisterButton;

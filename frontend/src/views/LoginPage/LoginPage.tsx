import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { logIn } from "../../utils/api/login";

import SocialButtons from "../../components/LoginComponents/SocialButtons";
import WelcomeText from "../../components/LoginComponents/WelcomeText";
import Email from "../../components/LoginComponents/InputFields/Email";
import Password from "../../components/LoginComponents/InputFields/Password";

import { VerticalDivider } from "./styles";
import "./LoginPage.css";

function LoginPage({ setToken }: any) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    function callLogIn() {
        logIn({ setToken }, email, password).then(response => {
            if (response) navigate("/students");
            else alert("Login failed");
        });
    }

    return (
        <div>
            <div className="login-page-content-container my-5">
                <WelcomeText />
                <div className="login mx-auto">
                    <SocialButtons />
                    <VerticalDivider />
                    <div className="register-form-input-fields">
                        <Email email={email} setEmail={setEmail} />
                        <Password password={password} setPassword={setPassword} />
                        <div className="no-account">
                            Don't have an account? Ask an admin for an invite link
                        </div>
                        <div>
                            <button className="login-button" onClick={callLogIn}>
                                Log In
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default LoginPage;

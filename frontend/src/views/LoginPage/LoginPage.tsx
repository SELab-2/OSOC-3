import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { logIn } from "../../utils/api/login";

import SocialButtons from "../../components/LoginComponents/SocialButtons";
import WelcomeText from "../../components/LoginComponents/WelcomeText";
import Email from "../../components/LoginComponents/InputFields/Email";
import Password from "../../components/LoginComponents/InputFields/Password";

import { LoginPageContainer, LoginContainer, EmailLoginContainer, VerticalDivider } from "./styles";
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
            <LoginPageContainer>
                <WelcomeText />
                <LoginContainer>
                    <SocialButtons />
                    <VerticalDivider />
                    <EmailLoginContainer>
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
                    </EmailLoginContainer>
                </LoginContainer>
            </LoginPageContainer>
        </div>
    );
}

export default LoginPage;

import { useState } from "react";
import "./LoginPage.css";
import { logIn } from "../../utils/api/login";
import { useNavigate } from "react-router-dom";

import SocialButtons from "../../components/LoginComponents/SocialButtons";
import WelcomeText from "../../components/LoginComponents/WelcomeText";
import { VerticalDivider } from "./styles";

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
                        <div>
                            <input
                                type="email"
                                name="email"
                                placeholder="Email"
                                value={email}
                                onChange={e => setEmail(e.target.value)}
                            />
                        </div>
                        <div>
                            <input
                                type="password"
                                name="password"
                                placeholder="Password"
                                value={password}
                                onChange={e => setPassword(e.target.value)}
                            />
                        </div>
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

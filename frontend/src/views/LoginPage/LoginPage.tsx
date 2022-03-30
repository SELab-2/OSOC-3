import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { axiosInstance } from "../../utils/api/api";
import "./LoginPage.css";

import { GoogleLoginButton, GithubLoginButton } from "react-social-login-buttons";

function LoginPage({ setToken }: any) {
    function logIn() {
        const payload = new FormData();
        payload.append("username", email);
        payload.append("password", password);

        axiosInstance
            .post("/login/token", payload)
            .then((response: any) => {
                setToken(response.data.accessToken);
            })
            .then(() => navigate("/students"))
            .catch(function (error: any) {
                console.log(error);
            });
    }
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const navigate = useNavigate();

    return (
        <div>
            <div className="login-page-content-container my-5">
                <div className="welcome-text mx-auto">
                    <h1 className={"mb-5"}>Hi!</h1>
                    <h3>
                        Welcome to the Open Summer of Code selections app. After you've logged in
                        with your account, we'll enable your account so you can get started. An
                        admin will verify you as quick as possible.
                    </h3>
                </div>
                <div className="login mx-auto">
                    <div className="socials-container">
                        <div className="socials">
                            <div className="google-login-container">
                                <GoogleLoginButton />
                            </div>
                            <GithubLoginButton />
                        </div>
                    </div>
                    <div className="border-right" />

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
                            <button className="login-button" onClick={logIn}>
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

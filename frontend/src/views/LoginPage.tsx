import { useState } from "react";

import { GoogleLoginButton, GithubLoginButton } from "react-social-login-buttons";

const axios = require("axios").default;

function LoginPage() {
    function logIn() {
        const payload = new FormData();
        payload.append("username", email);
        payload.append("password", password);

        axios
            .post("http://127.0.0.1:8000/login/token", payload)
            .then((response: any) => console.log(response))
            .catch(function (error: any) {
                console.log(error);
            });
    }

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    return (
        <div>
            <div className="login-page-content-container my-5">
                <div className="welcome-text mx-auto">
                    <h1 className={"mb-5"}>Hi!</h1>
                    <h3>
                        Welcome to the open Summer of Code selections app. After you've logged in
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

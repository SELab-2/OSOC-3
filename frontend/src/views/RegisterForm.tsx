import OSOCLetters from "../components/OSOCLetters";

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { axiosInstance } from "../utils/api/api";

import { GoogleLoginButton, GithubLoginButton } from "react-social-login-buttons";

function RegisterForm() {
    function register() {
        // Check if passwords are the same
        if (password !== confirmPassword) {
            alert("Passwords do not match");
            return;
        }
        // Basic email checker
        if (!/^\w+([\\.-]?\w+-)*@\w+([\\.-]?\w+)*(\.\w{2,3})+$/.test(email)) {
            alert("This is not a valid email");
            return;
        }

        // TODO this has to change to get the edition the invite belongs to
        const edition = "2022";
        const payload = new FormData();
        payload.append("username", email);
        payload.append("name", name);
        payload.append("password", password);
        payload.append("confirmPassword", confirmPassword);

        axiosInstance
            .post("/editions/" + edition + "/register/email", payload)
            .then((response: any) => console.log(response))
            .then(() => navigate("/pending"))
            .catch(function (error: any) {
                console.log(error);
            });
    }

    const [email, setEmail] = useState("");
    const [name, setName] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    const navigate = useNavigate();

    return (
        <div>
            <OSOCLetters />
            <div className="register-form-content-container">
                <h1 style={{ marginBottom: "15px" }}>Create an account</h1>
                <div style={{ marginBottom: "15px", color: "grey" }}>
                    Sign up with your social media account or email address
                </div>
                <div className="socials-container-register">
                    <div className="socials-register">
                        <GoogleLoginButton text="Register with Google" />
                        <GithubLoginButton text="Register with GitHub" />
                    </div>
                </div>

                <h2 style={{ margin: "15px" }}>or</h2>

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
                            type="text"
                            name="name"
                            placeholder="Name"
                            value={name}
                            onChange={e => setName(e.target.value)}
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
                    <div>
                        <input
                            type="password"
                            name="confirm_password"
                            placeholder="Confirm Password"
                            value={confirmPassword}
                            onChange={e => setConfirmPassword(e.target.value)}
                        />
                    </div>
                </div>
                <div>
                    <button onClick={register} className="register-button">
                        Register
                    </button>
                </div>
            </div>
        </div>
    );
}

export default RegisterForm;

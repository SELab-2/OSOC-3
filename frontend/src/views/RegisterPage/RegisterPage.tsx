import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { axiosInstance } from "../../utils/api/api";

import { GoogleLoginButton, GithubLoginButton } from "react-social-login-buttons";

interface RegisterFields {
    email: string;
    name: string;
    uuid: string;
    pw: string;
}

function RegisterPage() {
    function register(uuid: string) {
        // Check if passwords are the same
        if (password !== confirmPassword) {
            alert("Passwords do not match");
            return;
        }
        // Basic email checker
        if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
            alert("This is not a valid email");
            return;
        }

        // TODO this has to change to get the edition the invite belongs to
        const edition = "1";
        const payload: RegisterFields = { email: email, name: name, uuid: uuid, pw: password };

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

    const params = useParams();
    const uuid = params.uuid;

    const [validUuid, setUuid] = useState(false);

    axiosInstance.get("/editions/" + 1 + "/invites/" + uuid).then(response => {
        if (response.data.uuid === uuid) {
            setUuid(true);
        }
    });

    if (validUuid && uuid) {
        return (
            <div>
                <div className="register-form-content-container my-5">
                    <h1 className={"mb-3"}>Create an account</h1>

                    <div className={"mb-3"} style={{ color: "grey" }}>
                        Sign up with your social media account or email address. Your unique link is
                        not useable again ({uuid})
                    </div>
                    <div className="socials-container">
                        <div className="socials-register">
                            <GoogleLoginButton text="Register with Google" />
                            <div className={"border-right"} />
                            <GithubLoginButton text="Register with GitHub" />
                        </div>
                    </div>

                    <h2 className={"m-3"}>or</h2>

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
                        <button onClick={() => register(uuid)} className="register-button">
                            Register
                        </button>
                    </div>
                </div>
            </div>
        );
    } else return <div>Not a valid register url</div>;
}

export default RegisterPage;

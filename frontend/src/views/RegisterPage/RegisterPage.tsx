import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { register } from "../../utils/api/register";
import { validateRegistrationUrl } from "../../utils/api";

import { Email, Name, Password, ConfirmPassword } from "../../components/RegisterComponents";

import { GoogleLoginButton, GithubLoginButton } from "react-social-login-buttons";

function RegisterPage() {
    function callRegister(uuid: string) {
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
        register(edition, email, name, uuid, password)
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

    validateRegistrationUrl("1", uuid).then(response => {
        if (response) {
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
                        <Email email={email} setEmail={setEmail} />
                        <Name name={name} setName={setName} />
                        <Password password={password} setPassword={setPassword} />
                        <ConfirmPassword
                            confirmPassword={confirmPassword}
                            setConfirmPassword={setConfirmPassword}
                        />
                    </div>
                    <div>
                        <button onClick={() => callRegister(uuid)} className="register-button">
                            Register
                        </button>
                    </div>
                </div>
            </div>
        );
    } else return <div>Not a valid register url</div>;
}

export default RegisterPage;

import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import { register } from "../../utils/api/register";
import { validateRegistrationUrl } from "../../utils/api";

import {
    Email,
    Name,
    Password,
    ConfirmPassword,
    SocialButtons,
    InfoText,
    BadInviteLink,
} from "../../components/RegisterComponents";

import { RegisterFormContainer, Or, RegisterButton } from "./styles";
import { decodeRegistrationLink } from "../../utils/logic/registration";
import PendingPage from "../PendingPage";

/**
 * Page where a user can register a new account. If the uuid in the url is invalid,
 * this renders the [[BadInviteLink]] component instead.
 */
export default function RegisterPage() {
    const [validUuid, setValidUuid] = useState(false);
    const [pending, setPending] = useState(false);
    const params = useParams();
    const data = decodeRegistrationLink(params.uuid);

    // Form fields
    const [email, setEmail] = useState("");
    const [name, setName] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    useEffect(() => {
        async function validateUuid() {
            if (data) {
                const response = await validateRegistrationUrl(data.edition, data.uuid);
                if (response) {
                    setValidUuid(true);
                }
            }
        }
        if (!validUuid) {
            validateUuid();
        }
    });

    async function callRegister(edition: string, uuid: string) {
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

        try {
            const response = await register(edition, email, name, uuid, password);
            if (response) {
                setPending(true);
            }
        } catch (error) {
            console.log(error);
            alert("Something went wrong when creating your account");
        }
    }

    if (pending) {
        return <PendingPage />;
    }

    // Invalid link
    if (!(validUuid && data)) {
        return <BadInviteLink />;
    }

    return (
        <div>
            <RegisterFormContainer>
                <InfoText />
                <SocialButtons />
                <Or>or</Or>
                <Email email={email} setEmail={setEmail} />
                <Name name={name} setName={setName} />
                <Password password={password} setPassword={setPassword} />
                <ConfirmPassword
                    confirmPassword={confirmPassword}
                    setConfirmPassword={setConfirmPassword}
                    callRegister={() => callRegister(data.edition, data.uuid)}
                />
                <div>
                    <RegisterButton onClick={() => callRegister(data.edition, data.uuid)}>
                        Register
                    </RegisterButton>
                </div>
            </RegisterFormContainer>
        </div>
    );
}

import React, { useState } from "react";
import { getInviteLink } from "../../../utils/api/users/users";
import "./InviteUser.css";
import { InviteInput, InviteContainer } from "./styles";
import { ButtonsDiv, ErrorDiv, LinkDiv } from "./InviteUserComponents";

export default function InviteUser(props: { edition: string }) {
    const [email, setEmail] = useState("");
    const [valid, setValid] = useState(true);
    const [errorMessage, setErrorMessage] = useState("");
    const [loading, setLoading] = useState(false);
    const [link, setLink] = useState("");

    const changeEmail = function (email: string) {
        setEmail(email);
        setValid(true);
        setLink("");
        setErrorMessage("");
    };

    const sendInvite = async (copyInvite: boolean) => {
        if (/[^@\s]+@[^@\s]+\.[^@\s]+/.test(email)) {
            setLoading(true);
            try {
                const response = await getInviteLink(props.edition, email);
                if (copyInvite) {
                    await navigator.clipboard.writeText(response.mailTo);
                } else {
                    window.open(response.mailTo);
                }
                setLoading(false);
                setEmail("");
            } catch (error) {
                setLoading(false);
                setErrorMessage("Something went wrong");
            }
        } else {
            setValid(false);
            setErrorMessage("Invalid email");
        }
    };

    return (
        <div>
            <InviteContainer>
                <InviteInput
                    className={valid ? "" : "email-field-error"}
                    value={email}
                    onChange={e => changeEmail(e.target.value)}
                />
                <ButtonsDiv loading={loading} sendInvite={sendInvite} />
            </InviteContainer>
            <ErrorDiv errorMessage={errorMessage} />
            <LinkDiv link={link} />
        </div>
    );
}

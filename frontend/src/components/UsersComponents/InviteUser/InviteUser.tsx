import React, { useState } from "react";
import { getInviteLink } from "../../../utils/api/users/users";
import "./InviteUser.css";
import { InviteInput, InviteContainer } from "./styles";
import { ButtonsDiv, ErrorDiv, MessageDiv } from "./InviteUserComponents";

/**
 * A component to invite a user as coach to a given edition.
 * Contains an input field for the email address of the new user
 * and a button to get a mailto link which contains the invite link or just the invite link.
 * @param props.edition The edition whereto the person will be invited.
 */
export default function InviteUser(props: { edition: string }) {
    const [email, setEmail] = useState(""); // The email address which is entered
    const [valid, setValid] = useState(true); // The given email address is valid (or still being typed)
    const [errorMessage, setErrorMessage] = useState(""); // An error message
    const [loading, setLoading] = useState(false); // The invite link is being created
    const [message, setMessage] = useState(""); // A message to confirm link created

    const changeEmail = function (email: string) {
        setEmail(email);
        setValid(true);
        setErrorMessage("");
        setMessage("");
    };

    const sendInvite = async (copyInvite: boolean) => {
        if (/[^@\s]+@[^@\s]+\.[^@\s]+/.test(email)) {
            setLoading(true);
            try {
                const response = await getInviteLink(props.edition, email);
                if (copyInvite) {
                    await navigator.clipboard.writeText(response.inviteLink);
                    setMessage("Copied invite link for " + email);
                } else {
                    window.open(response.mailTo);
                    setMessage("Created mail for " + email);
                }
                setLoading(false);
                setEmail("");
            } catch (error) {
                setLoading(false);
                setErrorMessage("Something went wrong");
                setMessage("");
            }
        } else {
            setValid(false);
            setErrorMessage("Invalid email");
            setMessage("");
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
            <MessageDiv message={message} />
            <ErrorDiv errorMessage={errorMessage} />
        </div>
    );
}

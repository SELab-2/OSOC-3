import React, { useState } from "react";
import { getInviteLink } from "../../../utils/api/users/users";
import "./InviteUser.css";
import { InviteInput, InviteContainer, Error, MessageDiv } from "./styles";
import { ButtonsDiv } from "./InviteUserComponents";

/**
 * A component to invite a user as coach to a given edition.
 * Contains an input field for the email address of the new user.
 * and a button to get a mailto link which contains the invite link,
 * or to copy the invite link to clipboard.
 * @param props.edition The edition whereto the person will be invited.
 */
export default function InviteUser(props: { edition: string }) {
    const [email, setEmail] = useState(""); // The email address which is entered
    const [valid, setValid] = useState(true); // The given email address is valid (or still being typed)
    const [errorMessage, setErrorMessage] = useState(""); // An error message
    const [loading, setLoading] = useState(false); // The invite link is being created
    const [message, setMessage] = useState(""); // A message to confirm link created

    /**
     * Change the content of the email field.
     * Remove error and message (user is probably still typing).
     * @param email The string set in the input filed.
     */
    const changeEmail = function (email: string) {
        setEmail(email);
        setValid(true);
        setErrorMessage("");
        setMessage("");
    };

    /**
     * Check if the form of the email is valid.
     * Send a request to backend to get the invite link.
     * Depending on the copyInvite parameter, the recieved invite link will be put in an mailto,
     * or copied to the user's clipboard.
     * @param copyInvite Boolean to indicate wether the invite should be copied to clipboard or a mailto should be created.
     */
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
                    setMessage("Created email for " + email);
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
            <MessageDiv>
                {message}
                <Error>{errorMessage}</Error>
            </MessageDiv>
        </div>
    );
}

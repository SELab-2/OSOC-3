import React, { useState } from "react";
import { getInviteLink } from "../../../utils/api/users/users";
import { InviteContainer, MessageDiv, InputContainer } from "./styles";
import { ButtonsDiv } from "./InviteUserComponents";
import { SearchBar } from "../../Common/Forms";
import { toast } from "react-toastify";

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
                toast.error("Failed to create invite", {
                    toastId: "send_invite_failed",
                });
                setMessage("");
            }
        } else {
            setValid(false);
            toast.error("Invalid email address", {
                toastId: "invalid_email",
            });
            setMessage("");
        }
    };

    return (
        <div>
            <InviteContainer>
                <InputContainer>
                    <SearchBar
                        value={email}
                        onChange={e => changeEmail(e.target.value)}
                        isInvalid={!valid}
                        placeholder="Email address"
                    />
                </InputContainer>
                <ButtonsDiv loading={loading} sendInvite={sendInvite} />
            </InviteContainer>
            <MessageDiv>{message}</MessageDiv>
        </div>
    );
}

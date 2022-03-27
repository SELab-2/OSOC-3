import React, { useState } from "react";
import { getInviteLink } from "../../../utils/api/users";
import "./InviteUsers.css";
import { InviteInput, InviteButton, Loader, InviteContainer, Link, Error } from "./styles";

export default function InviteUser() {
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

    const sendInvite = async () => {
        if (/[^@\s]+@[^@\s]+\.[^@\s]+/.test(email)) {
            setLoading(true);
            getInviteLink("edition", email).then(ding => {
                setLink(ding);
                setLoading(false);
                // TODO: fix email stuff
            });
        } else {
            setValid(false);
            setErrorMessage("Invalid email");
        }
    };

    const buttonDiv = () => {
        let button;
        if (loading) {
            button = <Loader />;
        } else {
            button = (
                <div>
                    <InviteButton onClick={() => sendInvite()}>Send invite</InviteButton>
                </div>
            );
        }
        return button;
    };

    const errorDiv = () => {
        let errorDiv = null;
        if (errorMessage) {
            errorDiv = <Error>{errorMessage}</Error>;
        }
        return errorDiv;
    };

    const linkDiv = () => {
        let linkDiv = null;
        if (link) {
            linkDiv = <Link>{link}</Link>;
        }
        return linkDiv;
    };

    return (
        <div>
            <InviteContainer>
                <InviteInput
                    className={valid ? "" : "email-field-error"}
                    placeholder="Invite user by email"
                    value={email}
                    onChange={e => changeEmail(e.target.value)}
                />
                {buttonDiv()}
            </InviteContainer>
            {errorDiv()}
            {linkDiv()}
        </div>
    );
}

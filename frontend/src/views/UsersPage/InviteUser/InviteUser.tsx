import React, { useState } from "react";
import { getInviteLink } from "../../../utils/api/users";
import "./InviteUsers.css";
import { InviteInput, InviteButton, Loader, InviteContainer, Link, Error } from "./styles";

function ButtonDiv(props: { loading: boolean; onClick: () => void }) {
    let buttonDiv;
    if (props.loading) {
        buttonDiv = <Loader />;
    } else {
        buttonDiv = (
            <div>
                <InviteButton onClick={props.onClick}>Send invite</InviteButton>
            </div>
        );
    }
    return buttonDiv;
}

function ErrorDiv(props: { errorMessage: string }) {
    let errorDiv = null;
    if (props.errorMessage) {
        errorDiv = <Error>{props.errorMessage}</Error>;
    }
    return errorDiv;
}

function LinkDiv(props: { link: string }) {
    let linkDiv = null;
    if (props.link) {
        linkDiv = <Link>{props.link}</Link>;
    }
    return linkDiv;
}

export default function InviteUser(props: { edition: string | undefined }) {
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
            const ding = await getInviteLink("props.edition", email);
            setLink(ding);
            setLoading(false);
            // TODO: fix email stuff
        } else {
            setValid(false);
            setErrorMessage("Invalid email");
        }
    };

    return (
        <div>
            <div>{props.edition}</div>
            <InviteContainer>
                <InviteInput
                    className={valid ? "" : "email-field-error"}
                    value={email}
                    onChange={e => changeEmail(e.target.value)}
                />
                <ButtonDiv loading={loading} onClick={sendInvite} />
            </InviteContainer>
            <ErrorDiv errorMessage={errorMessage} />
            <LinkDiv link={link} />
        </div>
    );
}

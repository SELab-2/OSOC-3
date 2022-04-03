import { CopyButton, InviteButton, Loader } from "../styles";
import React from "react";

export default function ButtonsDiv(props: {
    loading: boolean;
    sendInvite: (copy: boolean) => void;
}) {
    if (props.loading) {
        return <Loader />;
    }
    return (
        <div>
            <InviteButton onClick={() => props.sendInvite(false)}>Send invite</InviteButton>
            <CopyButton onClick={() => props.sendInvite(true)}>Copy invite</CopyButton>
        </div>
    );
}

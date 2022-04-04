import { CopyButton, InviteButton, Loader } from "../styles";
import React from "react";

/**
 * A component to choice between sending an invite or copying it to clipboard.
 * @param props.loading Invite is being created.
 * @param props.sendInvite A function to send/copy the link.
 */
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

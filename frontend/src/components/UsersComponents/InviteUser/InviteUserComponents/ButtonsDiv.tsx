import { InviteButton, Loader } from "../styles";
import React from "react";
import { Button, ButtonGroup, Dropdown } from "react-bootstrap";

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
        <InviteButton>
            <Dropdown as={ButtonGroup} size="sm">
                <Button onClick={() => props.sendInvite(false)} variant="success">
                    Send invite
                </Button>

                <Dropdown.Toggle split variant="success" id="dropdown-split-basic" />

                <Dropdown.Menu>
                    <Dropdown.Item onClick={() => props.sendInvite(true)}>
                        Copy invite link
                    </Dropdown.Item>
                </Dropdown.Menu>
            </Dropdown>
        </InviteButton>
    );
}

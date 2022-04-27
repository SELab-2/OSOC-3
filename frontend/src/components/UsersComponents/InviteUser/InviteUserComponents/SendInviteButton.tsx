import { DropdownField, InviteButton } from "../styles";
import React from "react";
import { Button, ButtonGroup, Dropdown, Spinner } from "react-bootstrap";

/**
 * A component to choice between sending an invite or copying it to clipboard.
 * @param props.loading Invite is being created. Used to show a spinner.
 * @param props.sendInvite A function to send/copy the link.
 */
export default function SendInviteButton(props: {
    loading: boolean;
    sendInvite: (copy: boolean) => void;
}) {
    if (props.loading) {
        return <Spinner animation="border" />;
    }
    return (
        <InviteButton>
            <Dropdown as={ButtonGroup} size="sm">
                <Button onClick={() => props.sendInvite(false)} variant="success">
                    Send invite
                </Button>

                <Dropdown.Toggle split variant="success" id="dropdown-split-basic" />

                <Dropdown.Menu>
                    <DropdownField onClick={() => props.sendInvite(true)}>
                        Copy invite link
                    </DropdownField>
                </Dropdown.Menu>
            </Dropdown>
        </InviteButton>
    );
}

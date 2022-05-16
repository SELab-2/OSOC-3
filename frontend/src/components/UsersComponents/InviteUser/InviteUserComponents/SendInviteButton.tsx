import { DropdownField, InviteButton } from "../styles";
import React from "react";
import { ButtonGroup, Dropdown, Spinner } from "react-bootstrap";
import { CreateButton } from "../../../Common/Buttons";
import { DropdownToggle } from "../../../Common/Buttons/styles";

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
            <Dropdown as={ButtonGroup}>
                <CreateButton onClick={() => props.sendInvite(false)} showIcon={false}>
                    Send invite
                </CreateButton>

                <DropdownToggle split id="dropdown-split-basic" />

                <Dropdown.Menu>
                    <DropdownField onClick={() => props.sendInvite(true)}>
                        Copy invite link
                    </DropdownField>
                </Dropdown.Menu>
            </Dropdown>
        </InviteButton>
    );
}

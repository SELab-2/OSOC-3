import { DropdownField, InviteButton } from "../styles";
import React from "react";
import { ButtonGroup, Dropdown } from "react-bootstrap";
import { CreateButton } from "../../../Common/Buttons";
import { DropdownToggle } from "../../../Common/Buttons/styles";

/**
 * A component to choice between sending an invite or copying it to clipboard.
 * @param props.sendInvite A function to send/copy the link.
 */
export default function SendInviteButton(props: { sendInvite: (copy: boolean) => void }) {
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

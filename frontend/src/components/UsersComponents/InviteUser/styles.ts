import styled from "styled-components";
import { Dropdown } from "react-bootstrap";

export const InviteContainer = styled.div`
    clear: both;
`;

export const InviteInput = styled.input.attrs({
    name: "email",
    placeholder: "Invite user by email",
})`
    height: 30px;
    width: 200px;
    font-size: 13px;
    margin-top: 10px;
    margin-left: 10px;
    margin-right: 5px;
    text-align: center;
    border-radius: 5px;
    border-width: 0;
    float: left;
`;

export const MessageDiv = styled.div`
    margin-left: 10px;
    margin-top: 5px;
    height: fit-content;
    overflow: auto;
`;

export const Error = styled.div`
    color: var(--osoc_red);
`;

export const InviteButton = styled.div`
    padding-top: 10px;
`;

export const DropdownField = styled(Dropdown.Item)`
    color: white;
    transition: 200ms ease-out;

    &:hover {
        background-color: var(--osoc_blue);
        color: var(--osoc_green);
        transition: 200ms ease-in;
    }
`;

import styled from "styled-components";
import { MenuItem } from "react-bootstrap-typeahead";

export const StyledMenuItem = styled(MenuItem)`
    padding-top: 0;
    padding-bottom: 0;
    color: white;
    transition: 200ms ease-out;

    &:hover {
        background-color: var(--osoc_blue);
        color: var(--osoc_green);
        transition: 200ms ease-in;
    }
`;

export const NameDiv = styled.div``;

export const EmailDiv = styled.div`
    float: left;
`;

export const AuthTypeDiv = styled.div`
    float: right;
    margin-left: 5px;
`;

export const EmailAndAuthDiv = styled.div`
    width: max-content;
`;

export const DropdownEmailDiv = styled.div`
    font-size: small;
    margin-bottom: 5px;
`;

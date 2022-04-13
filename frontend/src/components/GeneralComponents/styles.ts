import styled from "styled-components";
import { MenuItem } from "react-bootstrap-typeahead";

export const StyledMenuItem = styled(MenuItem)`
    color: white;
    transition: 200ms ease-out;

    &:hover {
        background-color: var(--osoc_blue);
        color: var(--osoc_green);
        transition: 200ms ease-in;
    }
`;

export const NameDiv = styled.div`
    float: left;
`;

export const EmailDiv = styled.div`
    float: right;
`;

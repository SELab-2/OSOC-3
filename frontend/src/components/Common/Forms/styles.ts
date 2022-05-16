import styled from "styled-components";
import Form from "react-bootstrap/Form";

export const StyledFormControl = styled(Form.Control)`
    background-color: var(--osoc_blue);
    color: white;
    border-color: transparent;

    &:focus {
        background-color: var(--osoc_blue);
        color: white;
        border-color: var(--osoc_green);
        box-shadow: none;
    }

    &:invalid {
        border-color: var(--osoc_red);
        box-shadow: none;
    }
`;

export const StyledSearchBar = styled(Form.Control)`
    background-color: var(--osoc_blue);
    color: white;
    border: 2px solid #323252;

    &:focus {
        background-color: var(--osoc_blue);
        color: white;
        border-color: var(--osoc_green);
        box-shadow: none;
    }

    &:invalid {
        border-color: var(--osoc_red);
        box-shadow: none;
    }
`;

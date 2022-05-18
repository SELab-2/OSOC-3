import styled from "styled-components";
import Form from "react-bootstrap/Form";
import Multiselect from "multiselect-react-dropdown";
import "./styles.css";

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

    &:focus,
    &:hover,
    &:active {
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

export const StyledMultiSelect = styled(Multiselect).attrs({ variant: "dark" })`
    background-color: var(--osoc_blue);
    color: white;
`;

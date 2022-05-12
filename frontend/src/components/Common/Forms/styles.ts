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
`;

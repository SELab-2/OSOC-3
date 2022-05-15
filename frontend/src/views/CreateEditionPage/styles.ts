import styled from "styled-components";
import { Form, Button } from "react-bootstrap";

export const CreateEditionDiv = styled.div`
    width: 80%;
    max-width: 500px;
    margin: auto;
`;

export const FormGroup = styled(Form.Group)`
    margin-top: 20px;
    .form-control {
        background-color: #131329;
        color: white;
        border: none;
    }
`;

export const ButtonDiv = styled.div`
    margin: 15px auto;
    display: flex;
    width: fit-content;
    align-items: center;
    vertical-align: middle;
`;

export const CancelButton = styled(Button)`
    display: flex;
    align-items: center;
    margin-right: 5px;
    background-color: #131329;
    color: white;
    border-color: #131329;

    &:hover {
        background-color: #131325;
        color: white;
        border-color: #131325;
    }
`;

import styled from "styled-components";
import { Form } from "react-bootstrap";

export const Error = styled.div`
    color: var(--osoc_red);
    width: 100%;
    margin: 20px auto auto;
`;

export const CreateEditionDiv = styled.div`
    width: 80%;
    max-width: 500px;
    margin: auto;
`;

export const FormGroup = styled(Form.Group)`
    margin-top: 20px;
`;

export const ButtonDiv = styled.div`
    margin-top: 20px;
    margin-bottom: 20px;
    float: right;
`;

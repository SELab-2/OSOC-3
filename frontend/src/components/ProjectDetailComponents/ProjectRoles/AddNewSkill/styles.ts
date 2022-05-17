import { Form } from "react-bootstrap";
import styled from "styled-components";

export const AddNewSkillContainer = styled.div`
    border: 2px solid #1a1a36;
    border-radius: 5px;
    margin: 10px 20px;
    margin-top: 5vh;
    margin-left: 0;
    padding: 20px 20px 20px 20px;
    background-color: #323252;
    box-shadow: 5px 5px 15px #131329;
    display: flex;
    height: max-content;
    justify-content: center;
`;

export const NewSkill = styled.div`
    border: 2px solid #1a1a36;
    border-radius: 5px;
    margin: 10px 20px;
    margin-top: 5vh;
    margin-left: 0;
    padding: 20px 20px 20px 20px;
    background-color: #323252;
    box-shadow: 5px 5px 15px #131329;
    display: flex;
    align-items: center;
    height: max-content;
`;

export const StyledFormSelect = styled(Form.Select)`
    background-color: var(--osoc_blue);
    color: white;
    border-color: transparent;
    max-width: 25%;

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

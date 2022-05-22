import styled from "styled-components";
import { Form } from "react-bootstrap";

export const CardsGrid = styled.div`
    display: grid;
    grid-gap: 5px;
    grid-template-columns: repeat(auto-fit, minmax(375px, 1fr));
    grid-auto-flow: dense;
`;

export const ControlContainer = styled.div`
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 20px;
    margin-bottom: 10px;
`;

export const SearchFieldDiv = styled.div`
    margin-right: 10px;
    float: left;
    width: 15em;
`;

export const OwnProject = styled(Form.Check)`
    margin-top: 10px;
    margin-left: 20px;
    .form-check-input {
        color: black;
    }
`;

export const ProjectsContainer = styled.div`
    overflow: auto;
`;

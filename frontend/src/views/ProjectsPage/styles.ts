import styled from "styled-components";
import { Form } from "react-bootstrap";

export const CardsGrid = styled.div`
    display: grid;
    grid-gap: 5px;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    grid-auto-flow: dense;
`;

export const SearchField = styled.input`
    margin: 20px 5px 5px 20px;
    padding: 5px 10px;
    background-color: #131329;
    color: white;
    border: none;
    border-radius: 10px;
`

export const SearchButton = styled.button`
    padding: 5px 10px;
    background-color: #00bfff;
    color: white;
    border: none;
    border-radius: 10px;
`

export const CreateButton = styled.button`
    margin-left: 25px;
    padding: 5px 10px;
    background-color: #44dba4;
    color: white;
    border: none;
    border-radius: 10px;
`
export const OwnProject = styled(Form.Check)`
    margin-top: 10px;
    margin-left: 20px;
`

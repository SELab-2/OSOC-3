import styled from "styled-components";
import { Button } from "react-bootstrap";

export const SuggestionButtons = styled.div`
    display: flex;
    flex-direction: row;
    width: 100%;
    margin-top: 2%;
`;

export const ConfirmButton = styled(Button)`
    width: 30%;
    height: 30%;
    margin-left: 2%;
    margin-right: 2%;
`;

export const ConfirmActionTitle = styled.p`
    margin-top: 2%;
    font-size: 20px;
`;

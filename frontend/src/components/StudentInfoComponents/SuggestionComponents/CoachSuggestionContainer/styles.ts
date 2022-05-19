import styled from "styled-components";
import { Button } from "react-bootstrap";

export const SuggestionActionTitle = styled.p`
    font-size: 20px;
`;

export const YesButton = styled(Button)`
    background-color: var(--osoc_green);
    color: black;
    height: 5vh;
    width: 18vh;
    margin-right: 2%;
`;

export const MaybeButton = styled(Button)`
    background-color: var(--osoc_orange);
    color: black;
    height: 5vh;
    width: 18vh;
    margin-left: 2%;
    margin-right: 2%;
`;

export const NoButton = styled(Button)`
    background-color: var(--osoc_red);
    color: black;
    height: 5vh;
    width: 18vh;
    margin-left: 2%;
    margin-right: 2%;
`;

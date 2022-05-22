import styled from "styled-components";
import { HoverAnimation } from "../../../Common/styles";

export const SuggestionContainer = styled.div`
    background-color: #1a1a36;
    border-radius: 5px;
    margin-top: 10px;
    margin-right: 10px;
    text-align: center;
    padding: 7.5px 15px;
    max-width: 40vw;
`;

export const NameDeleteContainer = styled.div`
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 5px 0;
`;

export const DrafterContainer = styled.div`
    border-radius: 5px;
    padding: 15px;
    margin-right: auto;
    background-color: #0f0f30;
    display: flex;
    margin-bottom: 5px;
    width: 100%;
    overflow: auto;
    text-align: left;
    text-overflow: ellipsis;
`;

interface StudentNameProps {
    removed: boolean;
}

export const StudentName = styled.div<StudentNameProps>`
    ${HoverAnimation}
    overflow: auto;
    text-overflow: ellipsis;
    max-width: 80%;

    ${props =>
        !props.removed &&
        `    text-decoration: underline;

    &:hover {
        cursor: pointer;
        color: var(--osoc_green);
    }`}
`;

import styled from "styled-components";

export const ProjectPageContainer = styled.div`
    display: flex;
    height: 90vh;
`;

export const ProjectContainer = styled.div`
    width: 100%;
    margin: 20px;
    border: 5px;
    overflow: auto;
`;

export const GoBack = styled.div`
    display: flex;
    align-items: center;
    margin-bottom: 10px;
    max-width: max-content;

    :hover {
        cursor: pointer;
    }
`;

export const ClientsContainer = styled.div`
    display: flex;
    align-items: center;
    color: lightgray;
    overflow-x: auto;
`;

export const ClientContainer = styled.div`
    display: flex;
    margin-right: 2%;
`;

export const Client = styled.h5`
    width: max-content;
    margin-bottom: 0;
    margin-right: 0;
`;

export const NumberOfStudents = styled.div`
    display: flex;
    align-items: center;
`;

export const Suggestions = styled.div`
    min-height: 10vh;
`;

export const SuggestionContainer = styled.div`
    margin: 10px;
    background-color: #1a1a28;
    padding: 10px;
    max-width: 25%;
    overflow: auto;
`;

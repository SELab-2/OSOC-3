import styled from "styled-components";

export const ProjectContainer = styled.div`
    margin: 20px;
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

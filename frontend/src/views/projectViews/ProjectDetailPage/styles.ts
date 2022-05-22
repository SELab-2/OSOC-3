import styled from "styled-components";

export const ProjectPageContainer = styled.div`
    display: flex;
    height: 100vh;
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
    justify-content: space-between;
    margin-top: 10px;
    margin-right: 20px;
    max-width: 100%;
`;

export const NumberOfStudents = styled.div`
    display: flex;
    align-items: center;
`;

export const MoreInfoLink = styled.div`
    margin-top: 5px;
    margin-bottom: 20px;
`;

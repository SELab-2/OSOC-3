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

export const AddButton = styled.button`
    padding: 0 10px;
    background-color: #00bfff;
    color: white;
    border: none;
    margin-right: 10px;
    border-radius: 5px;
`;

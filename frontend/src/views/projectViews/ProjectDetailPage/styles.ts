import styled from "styled-components";

export const ProjectContainer = styled.div`
    margin: 20px;
`;

export const GoBack = styled.div`
    display: flex;
    align-items: center;
    margin-bottom: 5px;

    :hover {
        cursor: pointer;
    }
`;

export const Title = styled.h2`
    text-overflow: ellipsis;
    overflow: hidden;
`;

export const ClientContainer = styled.div`
    display: flex;
    align-items: center;
    color: lightgray;
    overflow-x: scroll;
`;

export const Client = styled.h5`
    margin-right: 1%;
`;

export const NumberOfStudents = styled.div`
    display: flex;
    align-items: center;
    margin-bottom: 4px;
`;

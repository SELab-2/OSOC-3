import styled from "styled-components";

export const ProjectContainer = styled.div`
    margin: 20px;
`;

export const GoBack = styled.div`
    display: flex;
    align-items: center;
    margin-bottom: 5px;
    max-width: max-content;

    :hover {
        cursor: pointer;
    }
`;

export const TitleContainer = styled.div`
    display: flex;
    align-items: center;
`;

export const Title = styled.h2`
    text-overflow: ellipsis;
    overflow: hidden;
    margin-right: 10px;
`;

export const Save = styled.button`
    padding: 2px 10px;
    max-height: 30px;
    background-color: #44dba4;
    color: white;
    border: none;
    margin-left: 5px;
    border-radius: 5px;
`;

export const Cancel = styled.button`
    padding: 2px 10px;
    max-height: 30px;
    background-color: #131329;
    color: white;
    border: none;
    margin-left: 5px;
    border-radius: 5px;
`;

export const Delete = styled.button`
    background-color: #f14a3b;
    padding: 5px 5px;
    border: 0;
    border-radius: 1px;
    max-height: 30;
    margin-left: 5px;
    display: flex;
    align-items: center;
`;

export const ClientContainer = styled.div`
    display: flex;
    align-items: center;
    color: lightgray;
    overflow-x: auto;
`;

export const Client = styled.h5`
    margin-right: 1%;
`;

export const NumberOfStudents = styled.div`
    display: flex;
    align-items: center;
    margin-bottom: 4px;
`;

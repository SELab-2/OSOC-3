import styled from "styled-components";

export const CoachesContainer = styled.div`
    display: flex;
    align-items: center;
    margin-top: 20px;
    overflow-x: auto;
    padding-bottom: 15px;
`;

export const CoachContainer = styled.div`
    background-color: #1a1a36;
    border-radius: 5px;
    margin-right: 10px;
    text-align: center;
    padding: 7.5px 15px;
    width: fit-content;
    max-width: 20vw;
    display: flex;
`;

export const CoachText = styled.div`
    overflow: auto;
    text-overflow: ellipsis;
    white-space: nowrap;
`;

export const RemoveButton = styled.button`
    padding: 0px 2.5px;
    background-color: #f14a3b;
    color: white;
    border: none;
    margin-left: 10px;
    border-radius: 1px;
    display: flex;
    align-items: center;
`;

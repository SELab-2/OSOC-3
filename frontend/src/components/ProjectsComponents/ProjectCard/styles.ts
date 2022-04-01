import styled from "styled-components";

export const CardContainer = styled.div`
    border: 2px solid #1a1a36;
    border-radius: 20px;
    margin: 20px;
    margin-bottom: 5px;
    padding: 20px 50px 20px 20px;
    background-color: #323252;
    box-shadow: 5px 5px 15px #131329;
`;

export const CoachesContainer = styled.div`
    display: flex;
    margin-top: 20px;
`;

export const CoachContainer = styled.div`
    background-color: #1a1a36;
    border-radius: 10px;
    margin-right: 10px;
    text-align: center;
    padding: 10px;
    max-width: 50%;
    text-overflow: ellipsis;
    overflow: hidden;
`;

export const Delete = styled.button`
    background-color: #f14a3b;
    padding: 5px 10px;
    border: 0;
    border-radius: 5px;
    margin-top: 20px;
    margin-left: 100%;
`;

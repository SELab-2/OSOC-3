import styled from "styled-components";

export const SkillContainer = styled.div`
    border-radius: 5px;
    margin-top: 10px;
    background-color: #1a1a36;
    padding: 5px 10px;
    width: 35vw;
    min-width: 300px;
`;

export const TopContainer = styled.div`
    display: flex;
    align-items: center;
    justify-content: space-between;
`;

export const TopLeftContainer = styled.div`
    max-width: 90%;
    display: flex;
    align-items: center;
`;

export const SkillName = styled.div`
    min-width: 20%;
    max-width: 75%;
    overflow-x: auto;
    text-overflow: ellipsis;
`;

export const Delete = styled.button`
    background-color: #f14a3b;
    border: 0;
    padding: 2.5px 2.5px;
    border-radius: 1px;
    color: white;
    display: flex;
    align-items: center;
`;

export const DescriptionContainer = styled.div`
    margin-bottom: 10px;
    max-width: 100%;
`;

export const DescriptionInput = styled.input`
    margin-top: 10px;
    padding: 5px 10px;
    background-color: #131329;
    color: white;
    border: none;
    border-radius: 5px;
    width: 100%;
`;

export const AmountInput = styled.input`
    margin: 5px 10px;
    padding: 2px 10px;
    background-color: #131329;
    color: white;
    border: none;
    border-radius: 5px;
    width: 100px;
`;

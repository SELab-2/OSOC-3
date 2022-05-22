import styled from "styled-components";

export const Input = styled.input`
    margin-top: 10px;
    padding: 5px 10px;
    background-color: #131329;
    color: white;
    border: none;
    border-radius: 5px;
    width: 35vw;
    min-width: 300px;
`;

export const AddButton = styled.button`
    padding: 5px 10px;
    background-color: #00bfff;
    color: white;
    border: none;
    margin-left: 5px;
    border-radius: 5px;
`;

export const ItemName = styled.div`
    height: auto;
    overflow-x: auto;
    text-overflow: ellipsis;
    margin: auto;
    margin-left: 5px;
    margin-right: 5px;
`;

export const AddedItem = styled.div`
    margin: 5px;
    margin-left: 0;
    padding: 5px;
    background-color: #1a1a36;
    width: 35vw;
    max-width: 50%;
    border-radius: 5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
`;

export const WarningContainer = styled.div`
    max-width: fit-content;
    margin-top: 10px;
`;

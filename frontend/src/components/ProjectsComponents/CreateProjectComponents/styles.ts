import styled from "styled-components";

export const Input = styled.input`
    margin-top: 10px;
    padding: 5px 10px;
    background-color: #131329;
    color: white;
    border: none;
    border-radius: 5px;
`;

export const AddButton = styled.button`
    padding: 5px 10px;
    background-color: #00bfff;
    color: white;
    border: none;
    margin-left: 5px;
    border-radius: 5px;
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

export const ItemName = styled.div`
    overflow-x: scroll;
    text-overflow: ellipsis;
`;

export const AddedItem = styled.div`
    margin: 5px;
    margin-left: 0;
    padding: 5px;
    background-color: #1a1a36;
    width: fit-content;
    max-width: 75%;
    border-radius: 5px;
    display: flex;
`;

export const WarningContainer = styled.div`
    max-width: fit-content;
    margin-top: 10px;
`;

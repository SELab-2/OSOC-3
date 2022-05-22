import styled from "styled-components";

export const ClientsContainer = styled.div`
    display: flex;
    align-items: center;
    max-width: 85%;
    overflow: auto;
`;

export const ClientContainer = styled.div`
    display: flex;
    align-items: center;
    margin-right: 2%;
    width: fit-content;
    max-width: 20vw;
`;

export const Client = styled.h5`
    margin-bottom: 0;
    margin-right: 0;
    overflow: auto;
    white-space: nowrap;
`;

export const RemoveButton = styled.button`
    padding: 0px 2.5px;
    background-color: transparent;
    color: lightgray;
    border: none;
    margin-left: 5px;
    border-radius: 1px;
    display: flex;
    align-items: center;
`;

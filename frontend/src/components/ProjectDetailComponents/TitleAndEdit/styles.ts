import styled from "styled-components";

export const TitleContainer = styled.div`
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    margin-right: 20px;
`;

export const Title = styled.h2`
    overflow: hidden;
    margin-right: 10px;
    max-height: 3.6em;
    line-height: 1.3em;
    :hover {
        overflow: auto;
    }
`;

export const TitleInput = styled.input`
    padding: 5px 10px;
    background-color: #131329;
    color: white;
    border: none;
    border-radius: 5px;
`;

export const EditDeleteContainer = styled.div`
    display: flex;
    align-items: center;
`;

export const Edit = styled.div`
    :hover {
        cursor: pointer;
    }
`;

export const Cancel = styled.button`
    padding: 5px 10px;
    background-color: #131329;
    color: white;
    border: none;
    margin-left: 5px;
    margin-right: 5px;
    border-radius: 5px;
    height: 38px;
`;

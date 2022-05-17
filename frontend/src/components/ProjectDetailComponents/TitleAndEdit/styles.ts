import styled from "styled-components";

export const TitleContainer = styled.div`
    display: flex;
    align-items: center;
    margin-bottom: 10px;
`;

export const Title = styled.h2`
    text-overflow: ellipsis;
    overflow: hidden;
    margin-right: 10px;
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

export const Save = styled.button`
    padding: 5px 10px;
    max-height: 35px;
    background-color: #44dba4;
    color: white;
    border: none;
    margin-left: 5px;
    border-radius: 5px;
`;

export const Cancel = styled.button`
    padding: 5px 10px;
    max-height: 35px;
    background-color: #131329;
    color: white;
    border: none;
    margin-left: 5px;
    border-radius: 5px;
`;

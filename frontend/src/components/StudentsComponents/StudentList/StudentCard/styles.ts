import styled from "styled-components";

export const CardStudent = styled.div`
    display: flex;
    flex-direction: row;
    margin: 10px;
    &:hover {
        cursor: pointer;
    }
    background-color: var(--card-color);
    box-shadow: 5px 5px 15px #131329;
    border-radius: 5px;
    border: 2px solid #1a1a36;
`;

export const CardStudentInfo = styled.div`
    display: flex;
    width: 100%;
    min-height: 75px;
    flex-direction: row;
`;

export const CardVerticalContainer = styled.div`
    width: 100%;
    display: flex;
    flex-direction: column;
`;

export const CardHorizontalContainer = styled.div`
    display: flex;
    width: 100%;
    flex-direction: row;
`;

export const CardStudentName = styled.p`
    width: 80%;
    font-size: 20px;
    margin-left: 5%;
    margin-top: 1%;
`;

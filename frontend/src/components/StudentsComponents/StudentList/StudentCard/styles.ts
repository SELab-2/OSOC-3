import styled from "styled-components";

export const CardStudent = styled.div`
    display: flex;
    flex-direction: row;
    margin: 10px;
    &:hover {
        cursor: pointer;
    }
    background-color: #15343f;
    border-radius: 15px;
    border: 1px solid #15202b;
`;

export const CardConfirmColorBlock = styled.div`
    position: sticky;
    height: 75px;
    background-color: var(--osoc_green);
    border: 1px solid var(--osoc_green);
    width: 30px;
    z-index: 1;
`;

export const CardSuggestionBar = styled.div`
    height: 2px;
    width: 240px;
    align-self: center;
    background: var(--osoc_green);
    margin-bottom: 15px;
`;

export const CardStudentInfo = styled.div`
    display: flex;
    width: 300px;
    min-height: 75px;
    flex-direction: row;
`;

export const CardVerticalContainer = styled.div`
    display: flex;
    flex-direction: column;
    margin-left: 37px;
    margin-top: 11px;
`;

export const CardHorizontalContainer = styled.div`
    display: flex;
    width: 100%;
    flex-direction: row;
`;

export const CardStudentName = styled.p`
    font-size: 20px;
    width: 230px;
    min-height: 30px;
`;

export const CardAmountSuggestions = styled.p`
    font-size: 20px;
`;

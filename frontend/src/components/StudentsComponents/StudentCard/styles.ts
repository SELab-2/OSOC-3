import styled from "styled-components";

export const CardStudent = styled.div`
    display: flex;
    flex-direction: row;
    margin: 10px;
`;

export const CardConfirmColorBlock = styled.div`
    position: absolute;
    height: 75px;
    background-color: var(--osoc_green);
    border: 1px solid var(--osoc_green);
    width: 30px;
    z-index: 1;
`;

export const CardSuggestionBar = styled.div`
    height: 2px;
    width: 250px;
    align-self: center;
    background: var(--osoc_green);
`;

export const CardStudentInfo = styled.div`
    display: flex;
    width: 300px;
    height: 75px;
    border: 2px solid var(--osoc_green);
    border-radius: 15px;
    flex-direction: row;
    background: var(--background_color);
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
`;

export const CardAmountSuggestions = styled.p`
    font-size: 20px;
    margin-left: 115px;
`;

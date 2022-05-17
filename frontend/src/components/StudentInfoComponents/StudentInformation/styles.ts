import styled from "styled-components";

export const StudentInformationContainer = styled.div`
    width: 100%;
    padding: 20px;
`;

export const FullName = styled.div`
    display: flex;
`;

export const FirstName = styled.h1`
    padding-right: 10px;
    color: var(--osoc_orange);
`;

export const LastName = styled.h1`
    padding-right: 5px;
    color: var(--osoc_orange);
`;

export const StudentLink = styled.p`
    font-size: 12px;
    align-self: flex-end;
    &:hover {
        cursor: pointer;
    }
`;

export const PreferedName = styled.p`
    font-size: 20px;
`;

export const StudentInfoTitle = styled.h4`
    color: var(--osoc_orange);
`;

export const SuggestionField = styled.p`
    font-size: 20px;
`;

export const PersonalInfoField = styled.div`
    width: 50%;
    display: flex;
`;

export const SubjectFields = styled.div`
    width: 30vh;
    display: flex;
    flex-direction: column;
`;

export const PersonalInformation = styled.div`
    display: flex;
    flex-direction: row;
`;

export const SubjectValues = styled.div`
    width: 30vh;
    display: flex;
    flex-direction: column;
`;

export const PersonalInfoFieldSubject = styled.p`
    min-width: 30%;
`;

export const PersonalInfoFieldValue = styled.p`
    margin-left: 1vh;
`;

export const RolesField = styled.div`
    display: flex;
`;

export const RolesValues = styled.ul`
    margin-left: 5%;
`;

export const RoleValue = styled.li``;

export const LineBreak = styled.div`
    background-color: #163542;
    height: 3px;
    width: 100%;
    margin-bottom: 30px;
    margin-top: 30px;
`;

export const DefinitiveDecisionContainer = styled.div`
    width: 40%;
`;

export const NameAndRemoveButtonContainer = styled.div`
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
`;

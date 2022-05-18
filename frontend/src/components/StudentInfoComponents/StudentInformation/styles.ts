import styled from "styled-components";
import { BsPersonFill } from "react-icons/bs";

export const InfoHeadContainer = styled.div`
    width: 100%;
    margin-bottom: 1.5%;
`;

export const StudentInformationContainer = styled.div`
    width: 100%;
    padding: 20px;
`;

export const PersonIcon = styled(BsPersonFill)`
    width: 15%;
    height: 15%;
    background: var(--osoc_red_darkened);
`;

export const NameContainer = styled.div`
    display: flex;
    align-items: center;
    margin-top: 1%;
    margin-left: 1%;
    width: 98%;
`;

export const AllName = styled.div`
    display: flex;
    flex-direction: column;
    margin-left: 2%;
`;

export const FullName = styled.div`
    display: flex;
`;

export const FirstName = styled.span`
    font-size: 250%;
    padding-right: 10px;
    color: white;
`;

export const LastName = styled.span`
    font-size: 250%;
    padding-right: 5px;
    color: white;
`;

export const PreferedName = styled.p`
    margin-left: 1%;
    font-size: 150%;
`;

export const StudentLink = styled.p`
    font-size: 12px;
    align-self: center;
    &:hover {
        cursor: pointer;
    }
`;

export const SuggestionField = styled.p`
    font-size: 20px;
    margin-bottom: 1%;
`;

export const SubjectFields = styled.div`
    width: 22vh;
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

export const PersonalInfoFieldValue = styled.p``;

export const RoleValue = styled.p`
    margin-left: 2%;
    font-size: 100%;
    margin-bottom: 1%;
`;

export const DefinitiveDecisionContainer = styled.div`
    width: 40%;
`;

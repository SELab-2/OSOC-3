import styled from "styled-components";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Card } from "react-bootstrap";
import { SuggestionColor, SuggestionEnum } from "../../../data/enums/suggestions";

export const InfoHeadContainer = styled.div`
    display: flex;
    width: 100%;
    margin-bottom: 1.5%;
`;

export const StudentInformationContainer = styled.div`
    width: 100%;
    padding: 20px;
`;

export const ActionsCard = styled(Card)`
    max-width: 100%;
`;

export const NameContainer = styled.div`
    display: flex;
    align-items: center;
    margin-top: 1%;
    margin-left: 1%;
    width: 100%;
`;

export const ActionContainer = styled.div`
    align-items: flex-end;
    flex-direction: column;
    display: flex;
    margin-top: 1%;
    min-width: fit-content;
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

export const CopyLinkContainer = styled.div`
    display: flex;
    width: fit-content;
    height: 40%;
    align-items: center;
    font-size: 12px;
    &:hover {
        cursor: pointer;
        color: var(--osoc_green);
        transition: 200ms ease-out;
    }
`;

export const StudentLink = styled.p`
    font-size: 12px;
`;

export const CopyIcon = styled(FontAwesomeIcon)`
    margin-left: 0.35vh;
    margin-bottom: 20%;
`;

export const PreferedName = styled.p`
    font-size: 20px;
`;

export const SuggestionField = styled.div`
    display: flex;
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
    font-size: 100%;
    margin-bottom: 1%;
`;

export const DefinitiveDecisionContainer = styled.div`
    width: 40%;
`;

export const SuggestionTextColor = styled.p<{ suggestion: number }>`
    color: ${p =>
        p.suggestion === SuggestionEnum.YES
            ? SuggestionColor.YES
            : p.suggestion === SuggestionEnum.MAYBE
            ? SuggestionColor.MAYBE
            : p.suggestion === SuggestionEnum.NO
            ? SuggestionColor.NO
            : "#FFFFFF"};
`;

export const SuggestionCoachAndArg = styled.p`
    margin-left: 10px;
`;

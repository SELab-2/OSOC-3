/* eslint-disable react-hooks/exhaustive-deps */
import React, { useEffect, useState } from "react";
import {
    FullName,
    FirstName,
    LastName,
    LineBreak,
    PreferedName,
    StudentInfoTitle,
    SuggestionField,
    StudentInformationContainer,
    PersonalInfoField,
    PersonalInfoFieldValue,
    PersonalInfoFieldSubject,
    RolesField,
    RolesValues,
    RoleValue,
    NameAndRemoveButtonContainer,
} from "./styles";
import { AdminDecisionContainer, CoachSuggestionContainer } from "../SuggestionComponents";
import { Student } from "../../../data/interfaces/students";
import { Suggestion } from "../../../data/interfaces/suggestions";
import { getSuggestions } from "../../../utils/api/suggestions";
import { useParams } from "react-router-dom";
import RemoveStudentButton from "../RemoveStudentButton/RemoveStudentButton";
import { useAuth } from "../../../contexts";
import { Role } from "../../../data/enums";

interface Props {
    currentStudent: Student;
}

/**
 * Component that renders all information of a student and all buttons to perform actions on this student.
 * @param props current student whose information needs to be showed.
 */
export default function StudentInformation(props: Props) {
    const { role } = useAuth();
    const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
    const params = useParams();
    const editionId = params.editionId;
    const studentId = params.id;

    /**
     * Get all the suggestion that were made on this student.
     */
    // eslint-disable-next-line react-hooks/exhaustive-deps
    async function callGetSuggestions() {
        try {
            const response = await getSuggestions(params.editionId!, params.id!);
            setSuggestions(response.suggestions);
        } catch (error) {
            console.log(error);
        }
    }

    /**
     * Get the string representation for a suggestion value.
     * @param suggestion
     */
    function suggestionToText(suggestion: number) {
        if (suggestion === 0) {
            return "Undecided";
        } else if (suggestion === 1) {
            return "Yes";
        } else if (suggestion === 2) {
            return "Maybe";
        } else if (suggestion === 3) {
            return "No";
        }
    }

    /**
     * fetch suggestions whenever an edition id or student id changes.
     */
    useEffect(() => {
        callGetSuggestions();
    }, [editionId, studentId]);

    if (!props.currentStudent) {
        return (
            <div>
                <h1>loading</h1>
            </div>
        );
    } else {
        console.log(props.currentStudent.skills);
        return (
            <StudentInformationContainer>
                <NameAndRemoveButtonContainer>
                    <FullName>
                        <FirstName>{props.currentStudent.firstName}</FirstName>
                        <LastName>{props.currentStudent.lastName}</LastName>
                    </FullName>
                    <RemoveStudentButton />
                </NameAndRemoveButtonContainer>
                <PreferedName>Preferred name: {props.currentStudent.preferredName}</PreferedName>
                <LineBreak />
                <StudentInfoTitle>Suggestions</StudentInfoTitle>
                {suggestions.map(suggestion => (
                    <SuggestionField key={suggestion.suggestionId}>
                        {suggestion.coach.name}: "{suggestionToText(suggestion.suggestion)}"{" "}
                        {suggestion.argumentation}
                    </SuggestionField>
                ))}
                <LineBreak />
                <StudentInfoTitle>Personal information</StudentInfoTitle>
                <PersonalInfoField>
                    <PersonalInfoFieldSubject>Email:</PersonalInfoFieldSubject>
                    <PersonalInfoFieldValue>
                        {props.currentStudent.emailAddress}
                    </PersonalInfoFieldValue>
                </PersonalInfoField>
                <PersonalInfoField>
                    <PersonalInfoFieldSubject>Phone number:</PersonalInfoFieldSubject>
                    <PersonalInfoFieldValue>
                        {props.currentStudent.phoneNumber}
                    </PersonalInfoFieldValue>
                </PersonalInfoField>
                <PersonalInfoField>
                    <PersonalInfoFieldSubject>Is an alumni?:</PersonalInfoFieldSubject>
                    <PersonalInfoFieldValue>
                        {props.currentStudent.alumni ? "Yes" : "No"}
                    </PersonalInfoFieldValue>
                </PersonalInfoField>
                <PersonalInfoField>
                    <PersonalInfoFieldSubject>Wants to be student coach?:</PersonalInfoFieldSubject>
                    <PersonalInfoFieldValue>
                        {props.currentStudent.wantsToBeStudentCoach ? "Yes" : "No"}
                    </PersonalInfoFieldValue>
                </PersonalInfoField>
                <LineBreak />
                <StudentInfoTitle>Skills</StudentInfoTitle>
                <RolesField>
                    Roles:
                    <RolesValues>
                        {props.currentStudent.skills.map(skill => (
                            <RoleValue>{skill.name}</RoleValue>
                        ))}
                    </RolesValues>
                </RolesField>
                <LineBreak />
                <div>
                    <CoachSuggestionContainer student={props.currentStudent} />
                    {role === Role.ADMIN ? <AdminDecisionContainer /> : <></>}
                </div>
            </StudentInformationContainer>
        );
    }
}

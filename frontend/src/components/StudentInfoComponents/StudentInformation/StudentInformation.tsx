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
    Role,
    NameAndRemoveButtonContainer,
} from "./styles";
import { AdminDecisionContainer, CoachSuggestionContainer } from "../SuggestionComponents";
import { Student } from "../../../data/interfaces/students";
import { Suggestion } from "../../../data/interfaces/suggestions";
import { getSuggestions } from "../../../utils/api/suggestions";
import { useParams } from "react-router-dom";
import RemoveStudentButton from "../RemoveStudentButton/RemoveStudentButton";

interface Props {
    currentStudent: Student;
}

/**
 * Component that renders all information of a student and all buttons to perform actions on this student.
 * @param props current student whose information needs to be showed.
 */
export default function StudentInformation(props: Props) {
    const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
    const params = useParams();

    /**
     * Get all the suggestion that were made on this student.
     */
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
    }, [params.editionId!, params.id!]);

    if (!props.currentStudent) {
        return (
            <div>
                <h1>loading</h1>
            </div>
        );
    } else {
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
                        <Role>Frontend</Role>
                        <Role>Design</Role>
                        <Role>Communication</Role>
                    </RolesValues>
                </RolesField>
                <LineBreak />
                <div>
                    <CoachSuggestionContainer student={props.currentStudent} />
                    <AdminDecisionContainer />
                </div>
            </StudentInformationContainer>
        );
    }
}

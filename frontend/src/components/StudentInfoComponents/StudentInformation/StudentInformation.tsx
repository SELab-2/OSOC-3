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
    PersonalInfoFieldValue,
    PersonalInfoFieldSubject,
    RolesField,
    RolesValues,
    RoleValue,
    NameAndRemoveButtonContainer,
    SubjectFields,
    SubjectValues,
    PersonalInformation,
} from "./styles";
import { AdminDecisionContainer, CoachSuggestionContainer } from "../SuggestionComponents";
import { Suggestion } from "../../../data/interfaces/suggestions";
import { getSuggestions } from "../../../utils/api/suggestions";
import RemoveStudentButton from "../RemoveStudentButton/RemoveStudentButton";
import { useAuth } from "../../../contexts";
import { Role } from "../../../data/enums";
import { Student } from "../../../data/interfaces/students";
import { getStudent } from "../../../utils/api/students";
import LoadSpinner from "../../Common/LoadSpinner";
import { toast } from "react-toastify";

/**
 * Component that renders all information of a student and all buttons to perform actions on this student.
 */
export default function StudentInformation(props: { studentId: number; editionId: string }) {
    const { role } = useAuth();

    const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
    const [student, setStudent] = useState<Student | undefined>(undefined);

    /**
     * Get all the suggestion that were made on this student.
     */
    async function getData() {
        const studentResponse = await toast.promise(getStudent(props.editionId, props.studentId), {
            error: "Failed to get details",
        });
        const suggestionsResponse = await toast.promise(
            getSuggestions(props.editionId, props.studentId),
            { error: "Failed to get suggestions" }
        );
        setStudent(studentResponse);
        setSuggestions(suggestionsResponse.suggestions);
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
        getData();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [props.studentId, props.editionId]);

    if (student === undefined) {
        return <LoadSpinner show={true} />;
    } else {
        return (
            <StudentInformationContainer>
                <NameAndRemoveButtonContainer>
                    <FullName>
                        <FirstName>{student.firstName}</FirstName>
                        <LastName>{student.lastName}</LastName>
                    </FullName>
                    <RemoveStudentButton studentId={props.studentId} editionId={props.editionId} />
                </NameAndRemoveButtonContainer>
                <PreferedName>Preferred name: {student.preferredName}</PreferedName>
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
                <PersonalInformation>
                    <SubjectFields>
                        <PersonalInfoFieldSubject>Email:</PersonalInfoFieldSubject>
                        <PersonalInfoFieldSubject>Phone number:</PersonalInfoFieldSubject>
                        <PersonalInfoFieldSubject>Is an alumni?:</PersonalInfoFieldSubject>
                        <PersonalInfoFieldSubject>
                            Wants to be student coach?:
                        </PersonalInfoFieldSubject>
                    </SubjectFields>
                    <SubjectValues>
                        <PersonalInfoFieldValue>{student.emailAddress}</PersonalInfoFieldValue>
                        <PersonalInfoFieldValue>{student.phoneNumber}</PersonalInfoFieldValue>
                        <PersonalInfoFieldValue>
                            {student.alumni ? "Yes" : "No"}
                        </PersonalInfoFieldValue>
                        <PersonalInfoFieldValue>
                            {student.wantsToBeStudentCoach ? "Yes" : "No"}
                        </PersonalInfoFieldValue>
                    </SubjectValues>
                </PersonalInformation>
                <LineBreak />
                <StudentInfoTitle>Skills</StudentInfoTitle>
                <RolesField>
                    Roles:
                    <RolesValues>
                        {student.skills.map(skill => (
                            <RoleValue key={skill.skillId}>{skill.name}</RoleValue>
                        ))}
                    </RolesValues>
                </RolesField>
                <LineBreak />
                <div>
                    <CoachSuggestionContainer student={student} />
                    {role === Role.ADMIN ? <AdminDecisionContainer /> : <></>}
                </div>
            </StudentInformationContainer>
        );
    }
}

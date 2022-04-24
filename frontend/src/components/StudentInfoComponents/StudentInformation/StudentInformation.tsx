import React, {useEffect} from "react";
import {
    FullName,
    FirstName,
    LastName,
    LineBreak,
    PreferedName,
    StudentInfoTitle,
    Suggestion,
    StudentInformationContainer,
    PersonalInfoField,
    PersonalInfoFieldValue,
    RolesField,
    RolesValues,
    Role,
} from "./styles";
import { AdminDecisionContainer, CoachSuggestionContainer } from "../SuggestionComponents";
import {Student} from "../../../data/interfaces/students";

interface Props {
    currentStudent: Student;
}

export default function StudentInformation(props: Props) {

    useEffect(() => {
        console.log(props)
    }, [props]);

    return (
        <StudentInformationContainer>
            <FullName>
                <FirstName>"Riley"</FirstName>
                <LastName>"Pacocha"</LastName>
            </FullName>
            <PreferedName>Prefered name: "Rey"</PreferedName>
            <LineBreak />
            <StudentInfoTitle>Suggestions</StudentInfoTitle>
            <Suggestion>
                Wow this student is really incredible! We should give her a project!
            </Suggestion>
            <Suggestion>
                Wow this student is really incredible! We should give her a project!
            </Suggestion>
            <Suggestion>
                Wow this student is really incredible! We should give her a project!
            </Suggestion>
            <LineBreak />
            <StudentInfoTitle>Personal information</StudentInfoTitle>
            <PersonalInfoField className="email-field">
                Email <PersonalInfoFieldValue>riley.pacocha@test.com</PersonalInfoFieldValue>
            </PersonalInfoField>
            <PersonalInfoField className="phonenumber-field">
                Phone number <PersonalInfoFieldValue>0123 456 789</PersonalInfoFieldValue>
            </PersonalInfoField>
            <PersonalInfoField className="alumni-field">
                Is an alumni? <PersonalInfoFieldValue>Yes</PersonalInfoFieldValue>
            </PersonalInfoField>
            <PersonalInfoField className="studentcoach-field">
                Wants to be student coach? <PersonalInfoFieldValue>Yes</PersonalInfoFieldValue>
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
                <CoachSuggestionContainer />
                <AdminDecisionContainer />
            </div>
        </StudentInformationContainer>
    );
}

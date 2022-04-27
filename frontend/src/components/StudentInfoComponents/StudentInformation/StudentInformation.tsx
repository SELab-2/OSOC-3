import React from "react";
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
    PersonalInfoFieldSubject,
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

    if (!props.currentStudent) {
        return <div><h1>loading</h1></div>
    } else {
        return (
            <StudentInformationContainer>
                <FullName>
                    <FirstName>{props.currentStudent.firstName}</FirstName>
                    <LastName>{props.currentStudent.lastName}</LastName>
                </FullName>
                <PreferedName>Prefered name: {props.currentStudent.preferredName}</PreferedName>
                <LineBreak/>
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
                <LineBreak/>
                <StudentInfoTitle>Personal information</StudentInfoTitle>
                <PersonalInfoField>
                    <PersonalInfoFieldSubject>Email:</PersonalInfoFieldSubject>
                    <PersonalInfoFieldValue>{props.currentStudent.emailAddress}</PersonalInfoFieldValue>
                </PersonalInfoField>
                <PersonalInfoField>
                    <PersonalInfoFieldSubject>Phone number:</PersonalInfoFieldSubject>
                    <PersonalInfoFieldValue>{props.currentStudent.phoneNumber}</PersonalInfoFieldValue>
                </PersonalInfoField>
                <PersonalInfoField>
                    <PersonalInfoFieldSubject>Is an alumni?:</PersonalInfoFieldSubject>
                    <PersonalInfoFieldValue>{props.currentStudent.alumni? "Yes": "No" }</PersonalInfoFieldValue>
                </PersonalInfoField>
                <PersonalInfoField>
                    <PersonalInfoFieldSubject>Wants to be student coach?:</PersonalInfoFieldSubject>
                    <PersonalInfoFieldValue>{props.currentStudent.wantsToBeStudentCoach? "Yes" : "No" }</PersonalInfoFieldValue>
                </PersonalInfoField>
                <LineBreak/>
                <StudentInfoTitle>Skills</StudentInfoTitle>
                <RolesField>
                    Roles:
                    <RolesValues>
                        <Role>Frontend</Role>
                        <Role>Design</Role>
                        <Role>Communication</Role>
                    </RolesValues>
                </RolesField>
                <LineBreak/>
                <div>
                    <CoachSuggestionContainer student={props.currentStudent}/>
                    <AdminDecisionContainer/>
                </div>
            </StudentInformationContainer>
        );
    }
}

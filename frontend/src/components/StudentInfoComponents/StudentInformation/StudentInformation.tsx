import React, { useEffect, useState } from "react";
import {
    FullName,
    FirstName,
    LastName,
    PreferedName,
    SuggestionField,
    StudentInformationContainer,
    PersonalInfoFieldValue,
    PersonalInfoFieldSubject,
    RoleValue,
    NameContainer,
    SubjectFields,
    SubjectValues,
    PersonalInformation,
    InfoHeadContainer,
    AllName,
    ActionContainer,
    ActionsCard,
    SuggestionTextColor,
    SuggestionCoachAndArg,
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
import StudentCopyLink from "../StudentCopyLink/StudentCopyLink";
import "./StudentInformation.css";
import { Card } from "react-bootstrap";
import StudentStateHistoryButton from "../StudentStateHistoryButton";
import QuestionsAndAnswers from "../QuestionsAndAnswers";
import { getQuestions } from "../../../utils/api/questions";
import { Question } from "../../../data/interfaces/questions";

/**
 * Component that renders all information of a student and all buttons to perform actions on this student.
 */
export default function StudentInformation(props: { studentId: number; editionId: string }) {
    const { role } = useAuth();

    const [questions, setQuestions] = useState<Question[]>([]);
    const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
    const [student, setStudent] = useState<Student | undefined>(undefined);

    async function getData() {
        const studentResponse = await toast.promise(getStudent(props.editionId, props.studentId), {
            error: "Failed to get details",
        });
        const suggestionsResponse = await toast.promise(
            getSuggestions(props.editionId, props.studentId),
            { error: "Failed to get suggestions" }
        );
        const answersResponse = await toast.promise(
            getQuestions(props.editionId, props.studentId),
            { error: "Failed to get suggestions" }
        );
        setStudent(studentResponse);
        setSuggestions(suggestionsResponse.suggestions);
        setQuestions(answersResponse.qAndA);
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
                <InfoHeadContainer>
                    <NameContainer>
                        <AllName>
                            <FullName>
                                <FirstName>{student.firstName}</FirstName>
                                <LastName>{student.lastName}</LastName>
                            </FullName>
                            {student.preferredName !== null && (
                                <div>
                                    <PreferedName>{student.preferredName}</PreferedName>
                                </div>
                            )}
                            <StudentCopyLink />
                        </AllName>
                    </NameContainer>
                    <ActionContainer>
                        <ActionsCard className="CardContainer" border="primary">
                            <Card.Header className="CardHeader">Actions</Card.Header>
                            <Card.Body className="CardBody">
                                <CoachSuggestionContainer student={student} />
                                {role === Role.ADMIN ? <AdminDecisionContainer /> : <></>}
                                <StudentStateHistoryButton
                                    editionId={props.editionId}
                                    studentId={props.studentId}
                                />
                            </Card.Body>
                        </ActionsCard>
                    </ActionContainer>
                </InfoHeadContainer>
                <Card className="CardContainer" border="primary">
                    <Card.Header className="CardHeader">Suggestions</Card.Header>
                    <Card.Body className="CardBody">
                        {suggestions.map(suggestion => (
                            <SuggestionField key={suggestion.suggestionId}>
                                <SuggestionTextColor suggestion={suggestion.suggestion}>
                                    {" "}
                                    {suggestionToText(suggestion.suggestion)}
                                </SuggestionTextColor>
                                <SuggestionCoachAndArg>
                                    {suggestion.coach.name}: "{suggestion.argumentation}"
                                </SuggestionCoachAndArg>
                            </SuggestionField>
                        ))}
                    </Card.Body>
                </Card>
                <Card className="CardContainer" border="primary">
                    <Card.Header className="CardHeader">Personal information</Card.Header>
                    <Card.Body className="CardBody">
                        <PersonalInformation>
                            <SubjectFields>
                                <PersonalInfoFieldSubject>Email</PersonalInfoFieldSubject>
                                <PersonalInfoFieldSubject>Phone number</PersonalInfoFieldSubject>
                                <PersonalInfoFieldSubject>Is an alumni?</PersonalInfoFieldSubject>
                                <PersonalInfoFieldSubject>
                                    Wants to be student coach?
                                </PersonalInfoFieldSubject>
                            </SubjectFields>
                            <SubjectValues>
                                <PersonalInfoFieldValue>
                                    {student.emailAddress}
                                </PersonalInfoFieldValue>
                                <PersonalInfoFieldValue>
                                    {student.phoneNumber}
                                </PersonalInfoFieldValue>
                                <PersonalInfoFieldValue>
                                    {student.alumni ? "Yes" : "No"}
                                </PersonalInfoFieldValue>
                                <PersonalInfoFieldValue>
                                    {student.wantsToBeStudentCoach ? "Yes" : "No"}
                                </PersonalInfoFieldValue>
                            </SubjectValues>
                        </PersonalInformation>
                    </Card.Body>
                </Card>
                <Card className="CardContainer" border="primary">
                    <Card.Header className="CardHeader">Skills</Card.Header>
                    <Card.Body className="CardBody">
                        {student.skills.map(skill => (
                            <RoleValue key={skill.skillId}>{skill.name}</RoleValue>
                        ))}
                    </Card.Body>
                </Card>
                <QuestionsAndAnswers questions={questions} />
                <RemoveStudentButton
                    student={student}
                    studentId={props.studentId}
                    editionId={props.editionId}
                />
            </StudentInformationContainer>
        );
    }
}

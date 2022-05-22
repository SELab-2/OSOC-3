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
import { getSuggestionById, getSuggestions } from "../../../utils/api/suggestions";
import RemoveStudentButton from "../RemoveStudentButton/RemoveStudentButton";
import { useAuth, useSockets } from "../../../contexts";
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
import { EventType, RequestMethod, WebSocketEvent } from "../../../data/interfaces/websockets";
import { useNavigate } from "react-router-dom";

const wsEventTypes = [EventType.STUDENT, EventType.STUDENT_SUGGESTION];

/**
 * Component that renders all information of a student and all buttons to perform actions on this student.
 */
export default function StudentInformation(props: { studentId: number; editionId: string }) {
    const { role } = useAuth();
    const { socket } = useSockets();
    const navigate = useNavigate();

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
     * Get all info about this student without showing toasts
     * Used in websockets
     */
    async function getDataNoToasts() {
        const student = await getStudent(props.editionId, props.studentId);
        const suggestionsResponse = await getSuggestions(props.editionId, props.studentId);
        setStudent(student);
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

    /**
     * Delete a suggestion from the list
     */
    function deleteSuggestion(id: string, suggestions: Suggestion[]): Suggestion[] {
        return suggestions.filter(s => s.suggestionId.toString() !== id);
    }

    /**
     * Find a suggestion in the list & update it
     */
    function findAndUpdateSuggestion(suggestion: Suggestion, list: Suggestion[]): Suggestion[] {
        const index = list.findIndex(s => s.suggestionId === suggestion.suggestionId);
        if (index === -1) return list;

        const copy = [...list];
        copy[index] = suggestion;
        return copy;
    }

    /**
     * Websockets
     */
    useEffect(() => {
        function listener(event: MessageEvent) {
            const data = JSON.parse(event.data) as WebSocketEvent;

            // Wrong type of event
            if (!wsEventTypes.includes(data.eventType)) return;
            // Event for another student
            if (data.pathIds.studentId !== props.studentId.toString()) return;

            if (data.eventType === EventType.STUDENT) {
                if (data.method === RequestMethod.DELETE) {
                    // Student deleted
                    navigate(`/editions/${props.editionId}/students`);
                    toast.info("This student was deleted by an admin.");
                    return;
                } else if (data.method === RequestMethod.POST) {
                    // Suggestion or decision created
                    getDataNoToasts().then();
                }
            }

            if (data.eventType === EventType.STUDENT_SUGGESTION) {
                if (data.method === RequestMethod.DELETE) {
                    // Suggestion deleted
                    setSuggestions(deleteSuggestion(data.pathIds.suggestionId!, suggestions));
                } else if (data.method === RequestMethod.PATCH) {
                    // Suggestion edited
                    // Fetch the updated suggestion & update it in the list
                    getSuggestionById(
                        props.editionId,
                        props.studentId.toString(),
                        data.pathIds.suggestionId!
                    ).then(suggestion =>
                        setSuggestions(findAndUpdateSuggestion(suggestion, suggestions))
                    );
                }
            }
        }

        socket?.addEventListener("message", listener);

        function removeListener() {
            if (socket) {
                socket.removeEventListener("message", listener);
            }
        }

        return removeListener;
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [socket, props.editionId, props.studentId, suggestions]);

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
                                {role === Role.ADMIN ? <AdminDecisionContainer /> : null}
                                {role === Role.ADMIN ? (
                                    <StudentStateHistoryButton
                                        editionId={props.editionId}
                                        studentId={props.studentId}
                                    />
                                ) : null}
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
                                    {suggestion.coach.name +
                                        (suggestion.argumentation
                                            ? ': "' + suggestion.argumentation + '"'
                                            : "")}
                                </SuggestionCoachAndArg>
                            </SuggestionField>
                        ))}
                        {suggestions.length === 0 ? (
                            <SuggestionField>
                                <SuggestionTextColor suggestion={-1}>
                                    No Suggestions yet
                                </SuggestionTextColor>
                            </SuggestionField>
                        ) : null}
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
                {role === Role.ADMIN ? (
                    <RemoveStudentButton
                        student={student}
                        studentId={props.studentId}
                        editionId={props.editionId}
                    />
                ) : null}
            </StudentInformationContainer>
        );
    }
}

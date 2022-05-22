import React from "react";
import { Card } from "react-bootstrap";
import { Question } from "../../../data/interfaces/questions";
import Answer from "./QuestionAnswer";

/**
 * Component that removes the current student.
 */
export default function QuestionsAndAnswers({ questions }: { questions: Question[] }) {
    return (
        <Card className="CardContainer" border="primary">
            <Card.Header className="CardHeader">Questions</Card.Header>
            <Card.Body className="CardBody">
                {questions.map((question, i) => (
                    <Answer key={i} question={question} />
                ))}
            </Card.Body>
        </Card>
    );
}

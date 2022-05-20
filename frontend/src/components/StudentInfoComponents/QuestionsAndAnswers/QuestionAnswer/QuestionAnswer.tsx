import React from "react";
import { Question } from "../../../../data/interfaces/questions";
import { Card } from "react-bootstrap";
import { QuestionAnswersContainer } from "./styles";

/**
 * Component that removes the current student.
 */
export default function QuestionAnswer({ question }: { question: Question }) {
    console.log(question);
    return (
        <Card className="CardContainer" border="primary">
            <Card.Header className="CardHeader">{question.question}</Card.Header>
            <Card.Body className="CardBody">
                <QuestionAnswersContainer>
                    {question.answers.map(answer => (
                        <p>{answer}</p>
                    ))}
                </QuestionAnswersContainer>
            </Card.Body>
        </Card>
    );
}

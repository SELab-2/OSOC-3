import React from "react";
import { Question } from "../../../../data/interfaces/questions";
import { Card } from "react-bootstrap";
import FileField from "../FileField/FileField";
import { QuestionAnswersContainer } from "./styles";

/**
 * Component that removes the current student.
 */
export default function QuestionAnswer({ question }: { question: Question }) {
    return (
        <div>
            {question.answers.length === 0 && question.files.length === 0 ? null : (
                <Card className="CardContainer" border="primary">
                    <Card.Header className="CardHeader">
                        <h4>{question.question}</h4>
                    </Card.Header>
                    <Card.Body className="CardBody">
                        <QuestionAnswersContainer>
                            {question.answers.map((answer, i) => (
                                <p key={i}>{answer}</p>
                            ))}
                            {question.files.length === 0 ? null : (
                                <div>
                                    {question.files.map((file, i) => (
                                        <FileField key={i} file={file} />
                                    ))}
                                </div>
                            )}
                        </QuestionAnswersContainer>
                    </Card.Body>
                </Card>
            )}
        </div>
    );
}

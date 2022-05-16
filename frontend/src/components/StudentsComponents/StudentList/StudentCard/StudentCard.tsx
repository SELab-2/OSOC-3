import React, { useEffect, useState } from "react";
import {
    CardStudent,
    CardStudentInfo,
    CardVerticalContainer,
    CardHorizontalContainer,
    CardStudentName,
} from "./styles";
import { useNavigate, useParams } from "react-router-dom";
import { Student } from "../../../../data/interfaces/students";
import SuggestionProgressBar from "../SuggestionProgressBar";

interface Props {
    student: Student;
}

/**
 * Card component that will be used to show a student in the students list.
 * @param props all information about a student.
 */
export default function StudentCard(props: Props) {
    const params = useParams();
    const navigate = useNavigate();
    const [nameColor, setNameColor] = useState("");

    useEffect(() => {
        const final = props.student.finalDecision;
        if (final === 0) {
            setNameColor("white");
        } else if (final === 1) {
            setNameColor("#44dba4"); // osoc green
        } else if (final === 2) {
            setNameColor("#fcb70f"); // osoc orange
        } else if (final === 3) {
            setNameColor("#f14a3b"); // osoc red
        }
    }, [props.student.finalDecision]);

    return (
        <>
            <CardStudent
                onClick={() =>
                    navigate(`/editions/${params.editionId}/students/${props.student.studentId}`)
                }
            >
                {/* <CardConfirmColorBlock /> */}
                <CardStudentInfo>
                    <CardVerticalContainer>
                        <CardHorizontalContainer>
                            <CardStudentName style={{ color: nameColor }}>
                                {props.student.firstName} {props.student.lastName}
                            </CardStudentName>
                        </CardHorizontalContainer>
                        <SuggestionProgressBar nrOfSuggestions={props.student.nrOfSuggestions} />
                    </CardVerticalContainer>
                </CardStudentInfo>
            </CardStudent>
        </>
    );
}

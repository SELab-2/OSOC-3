import React from "react";
import {
    CardStudent,
    CardStudentInfo,
    CardVerticalContainer,
    CardHorizontalContainer,
    CardStudentName,
} from "./styles";
import {useNavigate, useParams} from "react-router-dom";
import {NrSuggestions} from "../../../../data/interfaces/students";
import SuggestionProgressBar from "../SuggestionProgressBar";

interface Props {
    firstName: string;
    nrOfSuggestions: NrSuggestions;
    studentId: number;
}

export default function StudentCard(props: Props) {
    const params = useParams()
    const navigate = useNavigate();
    const params = useParams()

    return (
        <>
            <CardStudent onClick={() => navigate(`/editions/${params.editionId}/students/${props.studentId}`)}>
                {/* <CardConfirmColorBlock /> */}
                <CardStudentInfo>
                    <CardVerticalContainer>
                        <CardHorizontalContainer>
                            <CardStudentName>{props.firstName}</CardStudentName>
                        </CardHorizontalContainer>
                        <SuggestionProgressBar nrOfSuggestions={props.nrOfSuggestions}/>
                    </CardVerticalContainer>
                </CardStudentInfo>
            </CardStudent>
        </>
    );
}

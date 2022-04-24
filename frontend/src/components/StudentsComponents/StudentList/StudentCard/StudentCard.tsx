import React from "react";
import {
    CardStudent,
    CardStudentInfo,
    CardVerticalContainer,
    CardHorizontalContainer,
    CardSuggestionBar,
    CardStudentName,
    CardAmountSuggestions,
    AllSuggestions,
    SuggestionSignYes,
    SuggestionSignMaybe,
    SuggestionSignNo
} from "./styles";
import { useNavigate } from "react-router-dom";
import {NrSuggestions} from "../../../../data/interfaces/students";

interface Props {
    firstName: string;
    nrOfSuggestions: NrSuggestions;
    studentId: number;
}

export default function StudentCard(props: Props) {
    const navigate = useNavigate();

    return (
        <>
            <CardStudent onClick={() => navigate(`/editions/2022/students/${props.studentId}`)}>
                {/* <CardConfirmColorBlock /> */}
                <CardStudentInfo>
                    <CardVerticalContainer>
                        <CardHorizontalContainer>
                            <CardStudentName>{props.firstName}</CardStudentName>
                            <AllSuggestions>
                                <SuggestionSignYes>V</SuggestionSignYes>
                                <CardAmountSuggestions>
                                    {props.nrOfSuggestions.yes}
                                </CardAmountSuggestions>
                                <SuggestionSignMaybe>?</SuggestionSignMaybe>
                                <CardAmountSuggestions>
                                    {props.nrOfSuggestions.maybe}
                                </CardAmountSuggestions>
                                <SuggestionSignNo>X</SuggestionSignNo>
                                <CardAmountSuggestions>
                                    {props.nrOfSuggestions.no}
                                </CardAmountSuggestions>
                            </AllSuggestions>
                        </CardHorizontalContainer>
                        <CardSuggestionBar />
                    </CardVerticalContainer>
                </CardStudentInfo>
            </CardStudent>
        </>
    );
}

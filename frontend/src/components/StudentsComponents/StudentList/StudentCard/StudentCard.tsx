import React from "react";
import {
    CardStudent,
    CardStudentInfo,
    CardVerticalContainer,
    CardHorizontalContainer,
    CardSuggestionBar,
    CardStudentName,
    CardAmountSuggestions,
} from "./styles";
import { useNavigate } from "react-router-dom";

interface Props {
    name: string;
    amountOfSuggestions: number;
}

export default function StudentCard(props: Props) {
    const navigate = useNavigate();

    return (
        <>
            <CardStudent onClick={() => navigate(`/students/${props.name}`)}>
                {/* <CardConfirmColorBlock /> */}
                <CardStudentInfo>
                    <CardVerticalContainer>
                        <CardHorizontalContainer>
                            <CardStudentName>{props.name}</CardStudentName>
                            <CardAmountSuggestions>
                                {props.amountOfSuggestions}
                            </CardAmountSuggestions>
                        </CardHorizontalContainer>
                        <CardSuggestionBar />
                    </CardVerticalContainer>
                </CardStudentInfo>
            </CardStudent>
        </>
    );
}

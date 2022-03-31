import React from "react";
import {
    CardStudent,
    CardConfirmColorBlock,
    CardStudentInfo,
    CardVerticalContainer,
    CardHorizontalContainer,
    CardSuggestionBar,
    CardStudentName,
    CardAmountSuggestions,
} from "./styles";

export default function StudentCard() {
    return (
        <>
            <CardStudent>
                <CardConfirmColorBlock />
                <CardStudentInfo>
                    <CardVerticalContainer>
                        <CardHorizontalContainer>
                            <CardStudentName>Riley Pacocha</CardStudentName>
                            <CardAmountSuggestions>6</CardAmountSuggestions>
                        </CardHorizontalContainer>
                        <CardSuggestionBar />
                    </CardVerticalContainer>
                </CardStudentInfo>
            </CardStudent>
        </>
    );
}

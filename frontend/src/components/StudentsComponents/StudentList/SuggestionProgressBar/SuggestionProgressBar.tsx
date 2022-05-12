import React from "react";
import { NrSuggestions } from "../../../../data/interfaces/students";
import { SuggestionBarContainer } from "./styles";
import { ProgressBar } from "react-bootstrap";

interface Props {
    nrOfSuggestions: NrSuggestions;
}

function totalSuggestions(suggestions: NrSuggestions) {
    let total: number = 0;
    Object.entries(suggestions).forEach(([key, value]) => {
        total += value;
    });
    return total;
}

export default function SuggestionProgressBar(props: Props) {
    const amountSuggestions = totalSuggestions(props.nrOfSuggestions);
    const frequencyYes = (props.nrOfSuggestions.yes * 100) / amountSuggestions;
    const frequencyMaybe = (props.nrOfSuggestions.maybe * 100) / amountSuggestions;
    const frequencyNo = (props.nrOfSuggestions.no * 100) / amountSuggestions;
    console.log(props.nrOfSuggestions);
    return (
        <SuggestionBarContainer>
            <ProgressBar>
                <ProgressBar now={frequencyYes} variant={"success"} />
                <ProgressBar now={frequencyMaybe} variant={"warning"} />
                <ProgressBar now={frequencyNo} variant={"danger"} />
            </ProgressBar>
        </SuggestionBarContainer>
    );
}

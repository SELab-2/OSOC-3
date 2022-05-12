import React from "react";
import { NrSuggestions } from "../../../../data/interfaces/students";
import { SuggestionBarContainer } from "./styles";
import { ProgressBar } from "react-bootstrap";

interface Props {
    nrOfSuggestions: NrSuggestions;
}

/**
 * Count the total amount of suggestion (yes, maybe and no).
 * @param suggestions
 */
function totalSuggestions(suggestions: NrSuggestions) {
    let total: number = 0;
    Object.entries(suggestions).forEach(([key, value]) => {
        total += value;
    });
    return total;
}

/**
 * Component that shows a progressBar that weights all suggestions and shows how many of each there are.
 * @param props all the suggestions.
 */
export default function SuggestionProgressBar(props: Props) {
    const amountSuggestions = totalSuggestions(props.nrOfSuggestions);
    const frequencyYes = (props.nrOfSuggestions.yes * 100) / amountSuggestions;
    const frequencyMaybe = (props.nrOfSuggestions.maybe * 100) / amountSuggestions;
    const frequencyNo = (props.nrOfSuggestions.no * 100) / amountSuggestions;
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

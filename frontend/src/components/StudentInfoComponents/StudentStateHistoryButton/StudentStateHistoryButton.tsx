import React from "react";
import { OrangeButton } from "../../Common/Buttons";
import { StateContainer, StateTitle } from "./styles";
import { useNavigate } from "react-router-dom";

export default function StudentStateHistoryButton(props: { editionId: string; studentId: number }) {
    const navigate = useNavigate();

    return (
        <div>
            <StateTitle>State history of student</StateTitle>
            <StateContainer>
                <OrangeButton
                    onClick={() =>
                        navigate(`/editions/${props.editionId}/students/${props.studentId}/states`)
                    }
                    size="lg"
                >
                    State history
                </OrangeButton>
            </StateContainer>
        </div>
    );
}

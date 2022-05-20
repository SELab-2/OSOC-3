import { Edition } from "../../data/interfaces";
import { StyledReadonlyText } from "./styles";
import { useAuth } from "../../contexts";
import { Role } from "../../data/enums";

interface Props {
    edition: Edition;
    handleClick: () => void;
}

/**
 * Button on the [[EditionsPage]], displayed in an [[EditionsRow]], to toggle the readonly
 * state of an edition.
 */
export default function MarkReadonlyButton({ edition, handleClick }: Props) {
    const { role } = useAuth();
    const label = edition.readonly ? "READ-ONLY" : "EDITABLE";

    return (
        <StyledReadonlyText
            readonly={edition.readonly}
            onClick={handleClick}
            clickable={role === Role.ADMIN}
        >
            {label}
        </StyledReadonlyText>
    );
}

import { StyledNewEditionButton } from "./styles";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlus } from "@fortawesome/free-solid-svg-icons/faPlus";
import { IconProp } from "@fortawesome/fontawesome-svg-core";

interface Props {
    onClick: () => void;
}

/**
 * Button to create a new edition, redirects to the [[CreateEditionPage]].
 */
export default function NewEditionButton({ onClick }: Props) {
    return (
        <StyledNewEditionButton onClick={onClick}>
            <FontAwesomeIcon icon={faPlus as IconProp} className={"me-1"} /> Create new edition
        </StyledNewEditionButton>
    );
}

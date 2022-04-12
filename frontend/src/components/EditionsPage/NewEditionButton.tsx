import { StyledNewEditionButton } from "./styles";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlus } from "@fortawesome/free-solid-svg-icons/faPlus";
import { IconProp } from "@fortawesome/fontawesome-svg-core";
import { useAuth } from "../../contexts";
import { Role } from "../../data/enums";

interface Props {
    onClick: () => void;
}

/**
 * Button to create a new edition, redirects to the [[CreateEditionPage]].
 */
export default function NewEditionButton({ onClick }: Props) {
    const { role } = useAuth();

    // Only admins can create new editions
    if (role !== Role.ADMIN) {
        return null;
    }

    return (
        <StyledNewEditionButton onClick={onClick}>
            <FontAwesomeIcon icon={faPlus as IconProp} className={"me-1"} /> Create new edition
        </StyledNewEditionButton>
    );
}

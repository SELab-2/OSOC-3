import { Edition } from "../../data/interfaces";
import { DeleteButton } from "./styles";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTriangleExclamation } from "@fortawesome/free-solid-svg-icons/faTriangleExclamation";
import { IconProp } from "@fortawesome/fontawesome-svg-core";
import { useAuth } from "../../contexts";
import { Role } from "../../data/enums";

interface Props {
    edition: Edition;
}

export default function DeleteEditionButton(props: Props) {
    const { role } = useAuth();

    // Only admins can see this button
    if (role !== Role.ADMIN) {
        return null;
    }

    return (
        <DeleteButton>
            <FontAwesomeIcon icon={faTriangleExclamation as IconProp} /> Delete this edition
        </DeleteButton>
    );
}

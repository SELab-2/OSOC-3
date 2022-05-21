import { useAuth } from "../../contexts";
import { Role } from "../../data/enums";
import { CreateButton } from "../Common/Buttons";

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
        <CreateButton onClick={onClick} label={"Create new edition"} className={"ms-auto my-3"} />
    );
}

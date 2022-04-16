import { useAuth } from "../../contexts";
import NavDropdown from "react-bootstrap/NavDropdown";
import { StyledDropdownItem } from "./styles";
import { Role } from "../../data/enums";

interface Props {
    currentEdition: string;
}

/**
 * NavDropdown that links to the [[AdminsPage]] and [[UsersPage]].
 * This component is only rendered for admins.
 */
export default function UsersDropdown({ currentEdition }: Props) {
    const { role } = useAuth();

    // Only admins can see the dropdown because coaches can't
    // access these pages anyway
    if (role !== Role.ADMIN) {
        return null;
    }

    return (
        <NavDropdown title={"Users"}>
            <StyledDropdownItem href={"/admins"}>Admins</StyledDropdownItem>
            <StyledDropdownItem href={`/editions/${currentEdition}/users`}>
                Coaches
            </StyledDropdownItem>
        </NavDropdown>
    );
}

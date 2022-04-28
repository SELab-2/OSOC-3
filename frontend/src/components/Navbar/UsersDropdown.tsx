import NavDropdown from "react-bootstrap/NavDropdown";
import { StyledDropdownItem } from "./styles";
import { Role } from "../../data/enums";
import { LinkContainer } from "react-router-bootstrap";
import EditionNavLink from "./EditionNavLink";

interface Props {
    currentEdition: string;
    role: Role | null;
}

/**
 * NavDropdown that links to the [[AdminsPage]] and [[UsersPage]].
 * This component is only rendered for admins.
 */
export default function UsersDropdown({ currentEdition, role }: Props) {
    // Only admins can see the dropdown because coaches can't
    // access these pages anyway
    if (role !== Role.ADMIN) {
        return null;
    }

    return (
        <NavDropdown title={"Users"}>
            <LinkContainer to={"/admins"}>
                <StyledDropdownItem>Admins</StyledDropdownItem>
            </LinkContainer>
            <EditionNavLink currentEdition={currentEdition}>
                <LinkContainer to={`/editions/${currentEdition}/users`}>
                    <StyledDropdownItem>Coaches</StyledDropdownItem>
                </LinkContainer>
            </EditionNavLink>
        </NavDropdown>
    );
}

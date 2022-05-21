import NavDropdown from "react-bootstrap/NavDropdown";
import { LinkContainer } from "react-router-bootstrap";
import { StyledDropdownItem } from "./styles";
import { Role } from "../../data/enums";
import { Nav } from "react-bootstrap";

interface Props {
    isLoggedIn: boolean;
    currentEdition: string;
    role: Role | null;
}

/**
 * Dropdown in the [[Navbar]] that allows navigation to the [[StudentsPage]] and [[MailOverviewPage]].
 * @constructor
 */
export default function StudentsDropdown(props: Props) {
    if (!props.isLoggedIn || !props.currentEdition) return null;

    if (props.role === Role.COACH) {
        return (
            <LinkContainer to={`/editions/${props.currentEdition}/students`}>
                <Nav.Link>Students</Nav.Link>
            </LinkContainer>
        );
    } else if (props.role === Role.ADMIN) {
        return (
            <NavDropdown title={"Students"}>
                <LinkContainer to={`/editions/${props.currentEdition}/students`}>
                    <StyledDropdownItem>Students</StyledDropdownItem>
                </LinkContainer>
                <LinkContainer to={`/editions/${props.currentEdition}/students/states`}>
                    <StyledDropdownItem>States</StyledDropdownItem>
                </LinkContainer>
            </NavDropdown>
        );
    } else {
        return null;
    }
}

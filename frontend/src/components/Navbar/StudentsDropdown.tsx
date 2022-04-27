import NavDropdown from "react-bootstrap/NavDropdown";
import { LinkContainer } from "react-router-bootstrap";
import { StyledDropdownItem } from "./styles";

interface Props {
    isLoggedIn: boolean;
    currentEdition: string;
}

/**
 * Dropdown in the [[Navbar]] that allows navigation to the [[StudentsPage]] and [[MailOverviewPage]].
 * @constructor
 */
export default function StudentsDropdown(props: Props) {
    if (!props.isLoggedIn) return null;

    return (
        <NavDropdown title={"Students"}>
            <LinkContainer to={`/editions/${props.currentEdition}/students`}>
                <StyledDropdownItem>Students</StyledDropdownItem>
            </LinkContainer>
            <LinkContainer to={`/editions/${props.currentEdition}/students/emails`}>
                <StyledDropdownItem>Email History</StyledDropdownItem>
            </LinkContainer>
        </NavDropdown>
    );
}

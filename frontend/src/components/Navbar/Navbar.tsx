import Container from "react-bootstrap/Container";
import { BSNavbar, StyledDropdownItem } from "./styles";
import { useAuth } from "../../contexts";
import Brand from "./Brand";
import Nav from "react-bootstrap/Nav";
import NavDropdown from "react-bootstrap/NavDropdown";
import EditionDropdown from "./EditionDropdown";
import "./Navbar.css";
import LogoutButton from "./LogoutButton";
import { getCurrentEdition, setCurrentEdition } from "../../utils/session-storage/current-edition";
import { useParams } from "react-router-dom";

export default function Navbar() {
    const { isLoggedIn, editions } = useAuth();
    const params = useParams();

    // If the current URL contains an edition, use that
    // if not (eg. /editions), check SessionStorage
    // otherwise, use the most-recent edition from the auth response
    const currentEdition = params.editionId ? params.editionId : getCurrentEdition() || editions[0];

    // Set the value of the new edition in SessionStorage if useful
    if (currentEdition) {
        setCurrentEdition(currentEdition);
    }

    // Don't render Navbar if not logged in
    if (!isLoggedIn) {
        return null;
    }

    return (
        <BSNavbar>
            <Container>
                <Brand />
                {/* Make Navbar responsive (hamburger menu) */}
                <BSNavbar.Toggle aria-controls={"responsive-navbar-nav"} />
                <BSNavbar.Collapse id={"responsive-navbar-nav"}>
                    <Nav className={"ms-auto"}>
                        <EditionDropdown editions={editions} />
                        <Nav.Link href={"/editions"}>Editions</Nav.Link>
                        <Nav.Link href={`/editions/${currentEdition}/projects`}>Projects</Nav.Link>
                        <Nav.Link href={`/editions/${currentEdition}/students`}>Students</Nav.Link>
                        <NavDropdown title={"Users"}>
                            <StyledDropdownItem href={"/admins"}>Admins</StyledDropdownItem>
                            <StyledDropdownItem href={`/editions/${currentEdition}/users`}>
                                Coaches
                            </StyledDropdownItem>
                        </NavDropdown>
                        <LogoutButton />
                    </Nav>
                </BSNavbar.Collapse>
            </Container>
        </BSNavbar>
    );
}

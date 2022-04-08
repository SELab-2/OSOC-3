import Container from "react-bootstrap/esm/Container";
import { BSNavbar } from "./styles";
import { useAuth } from "../../contexts/auth-context";
import Brand from "./Brand";
import Nav from "react-bootstrap/Nav";
import { useState } from "react";
import NavDropdown from "react-bootstrap/NavDropdown";
import EditionDropdown from "./EditionDropdown";

export default function Navbar() {
    const { isLoggedIn, editions } = useAuth();
    const [currentEdition, setCurrentEdition] = useState<string>("edition");
    // const [currentEdition, setCurrentEdition] = useState<string>(editions[0]);

    // Don't render Navbar if not logged in
    if (!isLoggedIn) {
        return null;
    }

    return (
        <BSNavbar>
            <Container className={"mx-0"} fluid>
                <Brand />
                {/* Make Navbar responsive (hamburger menu) */}
                <BSNavbar.Toggle aria-controls={"responsive-navbar-nav"} />
                <BSNavbar.Collapse id={"responsive-navbar-nav"}>
                    <Nav className={"ms-auto"}>
                        <EditionDropdown
                            editions={editions}
                            currentEdition={currentEdition}
                            setCurrentEdition={setCurrentEdition}
                        />
                        <Nav.Link href={"/editions"}>Editions</Nav.Link>
                        <Nav.Link href={`/editions/${currentEdition}/projects`}>Projects</Nav.Link>
                        <Nav.Link href={`/editions/${currentEdition}/students`}>Students</Nav.Link>
                        <NavDropdown title={"Users"}>
                            <NavDropdown.Item href={"/admins"}>Admins</NavDropdown.Item>
                            <NavDropdown.Item href={`/editions/${currentEdition}/users`}>
                                Coaches
                            </NavDropdown.Item>
                        </NavDropdown>
                    </Nav>
                </BSNavbar.Collapse>
            </Container>
        </BSNavbar>
    );
}

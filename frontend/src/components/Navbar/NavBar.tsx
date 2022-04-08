import Container from "react-bootstrap/esm/Container";
import { BSNavbar } from "./styles";
import { useAuth } from "../../contexts/auth-context";
import Brand from "./Brand";
import Nav from "react-bootstrap/Nav";
import { useParams } from "react-router-dom";

export default function Navbar() {
    const { isLoggedIn } = useAuth();
    const { editionId } = useParams();

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
                        <Nav.Link>Projects</Nav.Link>
                    </Nav>
                </BSNavbar.Collapse>
            </Container>
        </BSNavbar>
    );
}

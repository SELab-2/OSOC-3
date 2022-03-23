import { Col, Container, Row } from "react-bootstrap";
import { FooterLink } from "./styles";

export default function FooterLinks() {
    return (
        <Container fluid className={"px-4 pb-5"}>
            <Row>
                <Col>
                    <h4>API</h4>
                    <FooterLink href={`${process.env.REACT_APP_BASE_URL}/redoc`}>
                        Documentation
                    </FooterLink>
                </Col>
            </Row>
        </Container>
    );
}

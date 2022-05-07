import { Col, Container, Row } from "react-bootstrap";
import { FooterLink } from "./styles";
import { BASE_URL } from "../../settings";

export default function FooterLinks() {
    return (
        <Container fluid className={"px-4 pb-4"}>
            <Row>
                <Col>
                    <h4>Documentation</h4>
                    <FooterLink href={`${BASE_URL}/redoc`}>Backend API</FooterLink>
                    <br />
                    {/* This link is always production because we don't host the docs locally */}
                    <FooterLink href={"https://sel2-3.ugent.be/typedoc/"}>Frontend</FooterLink>
                    <br />
                    <FooterLink
                        href={
                            "https://github.com/SELab-2/OSOC-3/blob/develop/files/user_manual.pdf"
                        }
                    >
                        User Manual
                    </FooterLink>
                </Col>
            </Row>
        </Container>
    );
}

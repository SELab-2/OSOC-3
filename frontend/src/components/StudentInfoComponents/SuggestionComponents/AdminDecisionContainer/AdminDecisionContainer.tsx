import React from "react";
import { Button, Form } from "react-bootstrap";
import { DefinitiveDecisionContainer } from "../../StudentInformation/styles";

export default function AdminDecisionContainer() {
    return (
        <div>
            <h4>Definitive decision by admin</h4>
            <DefinitiveDecisionContainer>
                <Form.Select aria-label="Default select example">
                    <option>Open this select menu</option>
                    <option value={0}>Yes</option>
                    <option value={1}>Maybe</option>
                    <option value={2}>No</option>
                </Form.Select>
                <Button variant="success" size="lg">
                    Confirm
                </Button>
            </DefinitiveDecisionContainer>
        </div>
    );
}

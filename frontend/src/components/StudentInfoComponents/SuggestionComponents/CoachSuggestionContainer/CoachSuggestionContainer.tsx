import React from "react";
import { Button, ButtonGroup } from "react-bootstrap";

export default function CoachSuggestionContainer() {
    return (
        <div>
            <h4>Make a suggestion on this student</h4>
            <ButtonGroup className="grid gap-sm-1">
                <Button variant="success" size="lg">
                    Yes
                </Button>
                <Button variant="warning" size="lg">
                    Maybe
                </Button>
                <Button variant="danger" size="lg">
                    No
                </Button>
            </ButtonGroup>
        </div>
    );
}

import React from "react";
import { ErrorContainer } from "../styles";

function ForbiddenPage() {
    return (
        <ErrorContainer>
            <h1>You don't have access to that page.</h1>
        </ErrorContainer>
    );
}

export default ForbiddenPage;

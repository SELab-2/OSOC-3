import React from "react";
import { ErrorContainer } from "../styles";

function ForbiddenPage() {
    return (
        <ErrorContainer>
            <h1>Stop right there!</h1>
            <h2>You don't have access to that page.</h2>
        </ErrorContainer>
    );
}

export default ForbiddenPage;

import React from "react";
import { ErrorContainer } from "../styles";

function NotFoundPage() {
    return (
        <ErrorContainer>
            <h1>Oops! This is awkward... </h1>
            <h2>You are looking for something that doesn't exist.</h2>
        </ErrorContainer>
    );
}

export default NotFoundPage;

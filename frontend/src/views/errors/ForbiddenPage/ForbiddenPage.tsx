import React from "react";
import { ErrorContainer } from "../styles";

/**
 * Page shown to users when they try to access a resource they aren't
 * authorized to. Examples include coaches performing admin actions,
 * or coaches going to urls for editions they aren't part of.
 */
export default function ForbiddenPage() {
    return (
        <ErrorContainer>
            <h1>Stop right there!</h1>
            <h2>You don't have access to that page.</h2>
        </ErrorContainer>
    );
}

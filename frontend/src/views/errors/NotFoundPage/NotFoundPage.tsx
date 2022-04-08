import React from "react";
import { ErrorContainer } from "../styles";

/**
 * Page shown when going to a url for a page that doesn't exist.
 */
export default function NotFoundPage() {
    return (
        <ErrorContainer>
            <h1>Oops! This is awkward... </h1>
            <h2>You are looking for something that doesn't exist.</h2>
        </ErrorContainer>
    );
}

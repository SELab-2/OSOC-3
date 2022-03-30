import React from "react";
import { ErrorMessage } from "./styles";

function ErrorPage() {
    return (
        <ErrorMessage>
            Oops! This is awkward... You are looking for something that doesn't actually exists.
        </ErrorMessage>
    );
}

export default ErrorPage;

import { Error } from "../styles";
import React from "react";

/**
 * A component which shows an error if there is one.
 * @param props.errorMessage The possible message.
 */
export default function ErrorDiv(props: { errorMessage: string }) {
    let errorDiv = null;
    if (props.errorMessage) {
        errorDiv = <Error>{props.errorMessage}</Error>;
    }
    return errorDiv;
}

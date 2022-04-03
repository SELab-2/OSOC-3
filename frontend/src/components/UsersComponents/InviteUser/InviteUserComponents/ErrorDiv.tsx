import { Error } from "../styles";
import React from "react";

export default function ErrorDiv(props: { errorMessage: string }) {
    let errorDiv = null;
    if (props.errorMessage) {
        errorDiv = <Error>{props.errorMessage}</Error>;
    }
    return errorDiv;
}

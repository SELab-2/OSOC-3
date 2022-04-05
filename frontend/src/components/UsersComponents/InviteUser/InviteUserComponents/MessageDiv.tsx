import { Message } from "../styles";
import React from "react";

/**
 * A component which shows a message if there is one.
 * @param props.message The possible message.
 */
export default function MessageDiv(props: { message: string }) {
    let messageDiv = null;
    if (props.message) {
        messageDiv = <Message>{props.message}</Message>;
    }
    return messageDiv;
}

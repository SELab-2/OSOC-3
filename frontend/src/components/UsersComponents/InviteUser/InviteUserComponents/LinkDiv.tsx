import { Link } from "../styles";
import React from "react";

export default function LinkDiv(props: { link: string }) {
    let linkDiv = null;
    if (props.link) {
        linkDiv = <Link>{props.link}</Link>;
    }
    return linkDiv;
}

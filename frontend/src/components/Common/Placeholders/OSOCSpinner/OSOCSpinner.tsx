import React from "react";
import { SpinningC } from "./styles";
import OsocLetterC from "../../../../images/letters/osoc_c.svg";

interface Props {
    children?: React.ReactNode;
    show: boolean;
}

/**
 * Loading spinner comprised of a spinning C from the OSOC logo, as on the OSOC-website.
 * This component can render children to easily hide a component if necessary
 */
export default function OSOCSpinner({ children, show }: Props) {
    if (show) {
        return <SpinningC src={OsocLetterC} />;
    }

    return <>{children}</>;
}

import React from "react";

interface Props {
    children: React.ReactNode;
    currentEdition?: string | undefined;
}

/**
 * Wrapper component for a NavLink that should only be displayed if
 * the current edition is defined.
 *
 * This means that when the user is not in any editions yet, the link
 * will be hidden.
 *
 * Any number of NavLinks can be included as children, it's unnecessary to wrap every
 * single link with this component.
 *
 * An example is the link that goes to the [[StudentsPage]].
 */
export default function EditionNavLink({ children, currentEdition }: Props) {
    if (!currentEdition) return null;
    return <>{children}</>;
}

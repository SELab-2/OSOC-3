import { useAuth } from "../../contexts";
import { Role } from "../../data/enums";
import React from "react";

/**
 * Message shown when the [[EditionsTable]] is empty.
 */
export default function EmptyEditionsTableMessage() {
    const { role } = useAuth();

    let message: React.ReactNode;

    // Show a different message to admins & coaches
    // admins are never part of any editions, coaches are never able to create an edition
    if (role === Role.ADMIN) {
        message = (
            <>
                There are no editions yet.
                <br />
                You can use the button above to create one.
            </>
        );
    } else {
        message = (
            <>
                It looks like you're not a part of any editions.
                <br />
                Contact an admin to receive an invite.
            </>
        );
    }

    return <div className={"mx-auto text-center"}>{message}</div>;
}

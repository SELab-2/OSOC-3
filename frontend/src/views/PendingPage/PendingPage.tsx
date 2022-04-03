import React from "react";
import "./PendingPage.css";

import {
    PendingPageContainer,
    PendingContainer,
    PendingTextContainer,
    PendingText,
} from "./styles";

/**
 * Page shown when your request to access an edition hasn't been accepted
 * (or rejected) yet.
 */
export default function PendingPage() {
    return (
        <div>
            <PendingPageContainer>
                <PendingContainer>
                    <PendingTextContainer>
                        <PendingText>
                            <h1>Your request is pending</h1>
                            <h1 className="pending-dot-1">.</h1>
                            <h1 className="pending-dot-2">.</h1>
                            <h1 className="pending-dot-3">.</h1>
                        </PendingText>
                    </PendingTextContainer>
                    <div>
                        <h1>Please wait until an admin approves your request!</h1>
                    </div>
                </PendingContainer>
            </PendingPageContainer>
        </div>
    );
}

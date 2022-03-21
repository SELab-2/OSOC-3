import React from "react";
import OSOCLetters from "../components/OSOCLetters";

function PendingPage() {
    return(
        <div>
            <OSOCLetters/>
            <div className="pending-page-content-container">
                <div className="pending-page-content">
                    <div className="pending-text">
                        <h1>Your request is pending</h1>
                        <h1 className="pending-dot-1">.</h1>
                        <h1 className="pending-dot-2">.</h1>
                        <h1 className="pending-dot-3">.</h1>
                    </div>
                    <h1>Please wait until an admin approves your request!</h1>
                </div>
            </div>
        </div>
    )
}

export default PendingPage
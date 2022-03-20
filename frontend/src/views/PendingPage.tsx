import React from "react";
import OSOCLetters from "../components/OSOCLetters";

function PendingPage() {
    return(
        <div>
            <OSOCLetters/>
            <div className="pending-page-content-container">
                <div className="pending-page-content">
                    <span>Your request is pending...</span>
                    <span>Please wait until an admin approves your request!</span>
                </div>
            </div>
        </div>
    )
}

export default PendingPage
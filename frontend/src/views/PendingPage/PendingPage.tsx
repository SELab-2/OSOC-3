import React from "react";
import "./PendingPage.css"

function PendingPage() {
    return(
        <div>
            <div className="pending-page-content-container">
                <div className="pending-page-content">
                    <div className="pending-text-container">
                        <div className="pending-text-content">
                            <h1>Your request is pending</h1>
                            <h1 className="pending-dot-1">.</h1>
                            <h1 className="pending-dot-2">.</h1>
                            <h1 className="pending-dot-3">.</h1>
                        </div>
                    </div>
                    <div>
                        <h1>Please wait until an admin approves your request!</h1>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default PendingPage
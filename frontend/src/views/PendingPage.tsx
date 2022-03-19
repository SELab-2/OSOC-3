import React from "react";
import logoO1 from "../images/letters/osoc_orange_o.svg";
import logoS from "../images/letters/osoc_s.svg";
import logoO2 from "../images/letters/osoc_red_o.svg";
import logoC from "../images/letters/osoc_c.svg";
function PendingPage() {
    return(
        <div>
            <img src={logoO1} alt="logoO1" className="osoc-logo-O1"/>
            <img src={logoS} alt="logoS" className="osoc-logo-S"/>
            <img src={logoO2} alt="logoO2" className="osoc-logo-O2"/>
            <img src={logoC} alt="logoC" className="osoc-logo-C"/>
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
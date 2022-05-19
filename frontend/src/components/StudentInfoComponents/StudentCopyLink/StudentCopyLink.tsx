import React from "react";
import { StudentLink, CopyIcon, CopyLinkContainer } from "../StudentInformation/styles";
import { IconProp } from "@fortawesome/fontawesome-svg-core";
import { faLink } from "@fortawesome/free-solid-svg-icons";
import { toast } from "react-toastify";

/**
 * Copy URL of current selected student.
 */
export default function StudentCopyLink() {
    function copyStudentLink() {
        navigator.clipboard.writeText(window.location.href);
        toast.success("Copied student URL to clipboard!", { autoClose: 1000 });
    }
    return (
        <CopyLinkContainer>
            <StudentLink onClick={copyStudentLink}>copy link</StudentLink>
            <CopyIcon icon={faLink as IconProp} className={"me-2"} />
        </CopyLinkContainer>
    );
}

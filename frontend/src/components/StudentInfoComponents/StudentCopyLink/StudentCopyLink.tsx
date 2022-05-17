import React from "react";
import { StudentLink } from "../StudentInformation/styles";

/**
 * Copy URL of current selected student.
 */
export default function StudentCopyLink() {
    function copyStudentLink() {
        navigator.clipboard.writeText(window.location.href);
    }
    return <StudentLink onClick={copyStudentLink}>copy student link</StudentLink>;
}

import React from "react";
import { StudentFile } from "../../../../data/interfaces/questions";
import { FileLink } from "./styles";

/**
 * Component that renders a file with his link
 */
export default function FileField({ file }: { file: StudentFile }) {
    return <FileLink href={file.url}>{file.filename}</FileLink>;
}

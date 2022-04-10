import { Form } from "react-bootstrap";
import React from "react";

export default function AlumniFilter({
    alumniFilter,
    setAlumniFilter,
}: {
    alumniFilter: boolean;
    setAlumniFilter: (value: boolean) => void;
}) {
    return (
        <div>
            <Form.Check
                type="checkbox"
                name="alumniFilter"
                label="Only alumni"
                onChange={e => setAlumniFilter(e.target.checked)}
            />
        </div>
    );
}

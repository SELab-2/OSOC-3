import { Form } from "react-bootstrap";
import React from "react";
import { setAlumniFilterStorage } from "../../../../utils/session-storage/student-filters";

/**
 * Component that filters the students list based on the alumni field.
 * @param alumniFilter
 * @param setAlumniFilter
 */
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
                checked={alumniFilter}
                onChange={e => {
                    setAlumniFilter(e.target.checked);
                    setAlumniFilterStorage(String(e.target.checked));
                    e.target.checked = alumniFilter;
                }}
            />
        </div>
    );
}

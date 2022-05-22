import { Form } from "react-bootstrap";
import React from "react";
import { setAlumniFilterStorage } from "../../../../utils/session-storage/student-filters";

/**
 * Component that filters the students list based on the alumni field.
 * @param alumniFilter
 * @param setAlumniFilter
 * @param setPage Function to set the page to fetch next
 */
export default function AlumniFilter({
    alumniFilter,
    setAlumniFilter,
    setPage,
}: {
    alumniFilter: boolean;
    setAlumniFilter: (value: boolean) => void;
    setPage: (page: number) => void;
}) {
    return (
        <div>
            <Form.Check
                type="checkbox"
                name="alumniFilter"
                label="Only alumni"
                checked={alumniFilter}
                id="alumni_filter"
                onChange={e => {
                    setAlumniFilter(e.target.checked);
                    setAlumniFilterStorage(String(e.target.checked));
                    e.target.checked = alumniFilter;
                    setPage(0);
                }}
            />
        </div>
    );
}

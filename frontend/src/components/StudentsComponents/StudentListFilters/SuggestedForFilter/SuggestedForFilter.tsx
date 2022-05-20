import { Form } from "react-bootstrap";
import React from "react";
import { setSuggestedFilterStorage } from "../../../../utils/session-storage/student-filters";

/**
 * Component that filters the students list based on the suggested for field.
 * @param suggestedFilter
 * @param setSuggestedFilter
 * @param setPage Function to set the page to fetch next
 */
export default function SuggestedForFilter({
    suggestedFilter,
    setSuggestedFilter,
    setPage,
}: {
    suggestedFilter: boolean;
    setSuggestedFilter: (value: boolean) => void;
    setPage: (page: number) => void;
}) {
    return (
        <div>
            <Form.Check
                type="checkbox"
                name="suggestedFilter"
                label="Students you've suggested for"
                checked={suggestedFilter}
                onChange={e => {
                    setSuggestedFilter(e.target.checked);
                    setSuggestedFilterStorage(String(e.target.checked));
                    e.target.checked = suggestedFilter;
                    setPage(0);
                }}
            />
        </div>
    );
}

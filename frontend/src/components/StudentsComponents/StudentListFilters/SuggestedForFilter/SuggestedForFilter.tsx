import { Form } from "react-bootstrap";
import React from "react";
import { setSuggestedFilterStorage } from "../../../../utils/session-storage/student-filters";

/**
 * Component that filters the students list based on the suggested for field.
 * @param suggestedFilter
 * @param setSuggestedFilter
 */
export default function SuggestedForFilter({
    suggestedFilter,
    setSuggestedFilter,
}: {
    suggestedFilter: boolean;
    setSuggestedFilter: (value: boolean) => void;
}) {
    return (
        <div>
            <Form.Check
                type="checkbox"
                name="suggestedFilter"
                label="Students you've suggested for"
                checked={suggestedFilter}
                id="suggested_for_filter"
                onChange={e => {
                    setSuggestedFilter(e.target.checked);
                    setSuggestedFilterStorage(String(e.target.checked));
                    e.target.checked = suggestedFilter;
                }}
            />
        </div>
    );
}

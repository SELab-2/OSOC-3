import { Form } from "react-bootstrap";
import React from "react";

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
                onChange={e => {
                    setSuggestedFilter(e.target.checked);
                    e.target.checked = suggestedFilter;
                }}
            />
        </div>
    );
}

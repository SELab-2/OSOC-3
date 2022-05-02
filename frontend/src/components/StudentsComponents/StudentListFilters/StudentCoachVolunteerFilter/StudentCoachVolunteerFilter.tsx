import { Form } from "react-bootstrap";
import React from "react";

export default function StudentCoachVolunteerFilter({
    studentCoachVolunteerFilter,
    setStudentCoachVolunteerFilter,
}: {
    studentCoachVolunteerFilter: boolean;
    setStudentCoachVolunteerFilter: (value: boolean) => void;
}) {
    return (
        <div>
            <Form.Check
                type="checkbox"
                name="studentCoachVolunteerFilter"
                label="Only student coach volunteer"
                checked={studentCoachVolunteerFilter}
                onChange={e => {
                    setStudentCoachVolunteerFilter(e.target.checked);
                    e.target.checked = studentCoachVolunteerFilter;
                }}
            />
        </div>
    );
}

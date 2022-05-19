import { Form } from "react-bootstrap";
import React from "react";
import { setStudentCoachVolunteerFilterStorage } from "../../../../utils/session-storage/student-filters";

/**
 * Component that filters the students list based on the student coach field.
 * @param studentCoachVolunteerFilter
 * @param setStudentCoachVolunteerFilter
 */
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
                    setStudentCoachVolunteerFilterStorage(String(e.target.checked));
                    e.target.checked = studentCoachVolunteerFilter;
                }}
            />
        </div>
    );
}

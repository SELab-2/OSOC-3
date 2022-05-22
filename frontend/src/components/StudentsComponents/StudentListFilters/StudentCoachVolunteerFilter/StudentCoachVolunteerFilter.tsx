import { Form } from "react-bootstrap";
import React from "react";
import { setStudentCoachVolunteerFilterStorage } from "../../../../utils/session-storage/student-filters";

/**
 * Component that filters the students list based on the student coach field.
 * @param studentCoachVolunteerFilter
 * @param setStudentCoachVolunteerFilter
 * @param setPage Function to set the page to fetch next
 */
export default function StudentCoachVolunteerFilter({
    studentCoachVolunteerFilter,
    setStudentCoachVolunteerFilter,
    setPage,
}: {
    studentCoachVolunteerFilter: boolean;
    setStudentCoachVolunteerFilter: (value: boolean) => void;
    setPage: (page: number) => void;
}) {
    return (
        <div>
            <Form.Check
                type="checkbox"
                name="studentCoachVolunteerFilter"
                label="Only student coach volunteer"
                checked={studentCoachVolunteerFilter}
                id="student_coach_filter"
                onChange={e => {
                    setStudentCoachVolunteerFilter(e.target.checked);
                    setStudentCoachVolunteerFilterStorage(String(e.target.checked));
                    e.target.checked = studentCoachVolunteerFilter;
                    setPage(0);
                }}
            />
        </div>
    );
}

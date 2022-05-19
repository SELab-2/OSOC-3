import React, { useEffect, useState } from "react";
import StudentList from "../StudentList";
import { Form } from "react-bootstrap";
import { StudentListSideMenu, StudentListLinebreak, FilterControls, MessageDiv } from "./styles";
import AlumniFilter from "./AlumniFilter/AlumniFilter";
import StudentCoachVolunteerFilter from "./StudentCoachVolunteerFilter/StudentCoachVolunteerFilter";
import NameFilter from "./NameFilter/NameFilter";
import RolesFilter from "./RolesFilter/RolesFilter";
import "./StudentListFilters.css";
import ResetFiltersButton from "./ResetFiltersButton/ResetFiltersButton";
import { Student } from "../../../data/interfaces/students";
import { useParams } from "react-router-dom";
import { toast } from "react-toastify";
import { getStudents } from "../../../utils/api/students";
import SuggestedForFilter from "./SuggestedForFilter/SuggestedForFilter";

/**
 * Component that shows the sidebar with all the filters and student list.
 */
export default function StudentListFilters() {
    const params = useParams();
    const [allStudents, setAllStudents] = useState<Student[]>([]);
    const [students, setStudents] = useState<Student[]>([]);
    const [loading, setLoading] = useState(false);
    const [moreDataAvailable, setMoreDataAvailable] = useState(true);
    const [allDataFetched, setAllDataFetched] = useState(false);
    const [page, setPage] = useState(0);

    const [nameFilter, setNameFilter] = useState("");
    const [rolesFilter, setRolesFilter] = useState<number[]>([]);
    const [alumniFilter, setAlumniFilter] = useState(false);
    const [studentCoachVolunteerFilter, setStudentCoachVolunteerFilter] = useState(false);
    const [suggestedFilter, setSuggestedFilter] = useState(false);

    /**
     * Request all students with selected filters
     */
    async function getData(requested: number) {
        const filterChanged = requested === -1;
        const requestedPage = requested === -1 ? 0 : page;

        if (loading && !filterChanged) {
            return;
        }

        if (allDataFetched) {
            const tempStudents = allStudents
                .filter(student =>
                    (student.firstName + " " + student.lastName)
                        .toUpperCase()
                        .includes(nameFilter.toUpperCase())
                )
                .filter(student => !alumniFilter || student.alumni === alumniFilter)
                .filter(
                    student =>
                        !studentCoachVolunteerFilter ||
                        student.wantsToBeStudentCoach === studentCoachVolunteerFilter
                );

            if (rolesFilter.length === 0) {
                setStudents(tempStudents);
            } else {
                const newStudents: Student[] = [];
                for (const student of tempStudents) {
                    for (const skill of student.skills) {
                        if (rolesFilter.includes(skill.skillId)) {
                            newStudents.push(student);
                            break;
                        }
                    }
                }
                setStudents(newStudents);
            }
            setMoreDataAvailable(false);
            return;
        }

        setLoading(true);

        try {
            const response = await getStudents(
                params.editionId!,
                nameFilter,
                rolesFilter,
                alumniFilter,
                studentCoachVolunteerFilter,
                suggestedFilter,
                requestedPage
            );

            if (response.students.length === 0 && !filterChanged) {
                setMoreDataAvailable(false);
            }
            if (page === 0 || filterChanged) {
                setStudents(response.students);
            } else {
                setStudents(students.concat(response.students));
            }

            // If no filters are set, allStudents can be changed
            if (
                nameFilter === "" &&
                rolesFilter.length === 0 &&
                !alumniFilter &&
                !studentCoachVolunteerFilter &&
                !suggestedFilter
            ) {
                if (response.students.length === 0) {
                    setAllDataFetched(true);
                }
                if (page === 0) {
                    setAllStudents(response.students);
                } else {
                    setAllStudents(allStudents.concat(response.students));
                }
            }

            setPage(page + 1);
        } catch (error) {
            toast.error("Failed to get students.", { toastId: "fetch_students_failed" });
        }
        setLoading(false);
    }

    /**
     * fetch students again when a filter changes
     */
    useEffect(() => {
        setPage(0);
        setMoreDataAvailable(true);
        getData(-1);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [nameFilter, rolesFilter, alumniFilter, studentCoachVolunteerFilter, suggestedFilter]);

    let list;
    if (students.length === 0) {
        list = <MessageDiv>No students found</MessageDiv>;
    } else {
        list = (
            <StudentList
                students={students}
                getMoreData={getData}
                moreDataAvailable={moreDataAvailable}
            />
        );
    }

    return (
        <StudentListSideMenu>
            <NameFilter nameFilter={nameFilter} setNameFilter={setNameFilter} />
            <RolesFilter setRolesFilter={setRolesFilter} />
            <Form.Group>
                <AlumniFilter alumniFilter={alumniFilter} setAlumniFilter={setAlumniFilter} />
                <SuggestedForFilter
                    suggestedFilter={suggestedFilter}
                    setSuggestedFilter={setSuggestedFilter}
                />
                <StudentCoachVolunteerFilter
                    studentCoachVolunteerFilter={studentCoachVolunteerFilter}
                    setStudentCoachVolunteerFilter={setStudentCoachVolunteerFilter}
                />
            </Form.Group>
            <StudentListLinebreak />
            <FilterControls>
                <ResetFiltersButton
                    setNameFilter={setNameFilter}
                    setAlumniFilter={setAlumniFilter}
                    setStudentCoachVolunteerFilter={setStudentCoachVolunteerFilter}
                />
            </FilterControls>
            {list}
        </StudentListSideMenu>
    );
}

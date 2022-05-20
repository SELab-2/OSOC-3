import React, { useEffect, useState } from "react";
import StudentList from "../StudentList";
import { Form } from "react-bootstrap";
import { StudentListSideMenu, StudentListLinebreak, FilterControls, MessageDiv } from "./styles";
import AlumniFilter from "./AlumniFilter/AlumniFilter";
import StudentCoachVolunteerFilter from "./StudentCoachVolunteerFilter/StudentCoachVolunteerFilter";
import NameFilter from "./NameFilter/NameFilter";
import RolesFilter, { DropdownRole } from "./RolesFilter/RolesFilter";
import "./StudentListFilters.css";
import ResetFiltersButton from "./ResetFiltersButton/ResetFiltersButton";
import { Student } from "../../../data/interfaces/students";
import { useParams } from "react-router-dom";
import { toast } from "react-toastify";
import { getStudents } from "../../../utils/api/students";
import SuggestedForFilter from "./SuggestedForFilter/SuggestedForFilter";
import {
    getAlumniFilter,
    getConfirmFilter,
    getNameFilter,
    getRolesFilter,
    getStudentCoachVolunteerFilter,
    getSuggestedFilter,
} from "../../../utils/session-storage/student-filters";
import ConfirmFilters from "./ConfirmFilters/ConfirmFilters";
import LoadSpinner from "../../Common/LoadSpinner";

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
    const [controller, setController] = useState<AbortController | undefined>(undefined);

    const [nameFilter, setNameFilter] = useState(getNameFilter());
    const [rolesFilter, setRolesFilter] = useState<DropdownRole[]>(getRolesFilter());
    const [alumniFilter, setAlumniFilter] = useState(getAlumniFilter());
    const [studentCoachVolunteerFilter, setStudentCoachVolunteerFilter] = useState(
        getStudentCoachVolunteerFilter()
    );
    const [suggestedFilter, setSuggestedFilter] = useState(getSuggestedFilter());
    const [confirmFilter, setConfirmFilter] = useState<DropdownRole[]>(getConfirmFilter());

    /**
     * Request all students with selected filters
     */
    async function getData(requested: number, edChange: boolean = false) {
        const filterChanged = requested === -1;
        const requestedPage = requested === -1 ? 0 : page;

        if (loading && !filterChanged) {
            return;
        }

        if (allDataFetched && !edChange) {
            const tempStudents = allStudents
                .filter(student =>
                    (student.firstName + " " + student.lastName)
                        .toUpperCase()
                        .includes(nameFilter!.toUpperCase())
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
                        rolesFilter.forEach(dropdownValue => {
                            if (dropdownValue.value === skill.skillId) {
                                newStudents.push(student);
                            }
                        });
                    }
                }
                setStudents(newStudents);
            }
            setMoreDataAvailable(false);
            return;
        }

        setLoading(true);

        if (controller !== undefined) {
            controller.abort();
        }
        const newController = new AbortController();
        setController(newController);

        const response = await toast.promise(
            getStudents(
                params.editionId!,
                nameFilter,
                rolesFilter,
                alumniFilter,
                studentCoachVolunteerFilter,
                suggestedFilter,
                confirmFilter,
                requestedPage,
                newController
            ),
            { error: "Failed to retrieve students" }
        );

        if (response !== null) {
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
                confirmFilter.length === 0 &&
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
        } else {
            setMoreDataAvailable(false);
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
    }, [
        nameFilter,
        rolesFilter,
        alumniFilter,
        studentCoachVolunteerFilter,
        suggestedFilter,
        confirmFilter,
    ]);

    useEffect(() => {
        setStudents([]);
        setAllStudents([]);
        setPage(0);
        setAllDataFetched(false);
        setMoreDataAvailable(true);
        getData(-1, true);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [params.editionId]);

    let list;
    if (students.length === 0) {
        if (loading) {
            list = <LoadSpinner show={true} />;
        } else {
            list = <MessageDiv>No students found</MessageDiv>;
        }
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
            <NameFilter nameFilter={nameFilter} setNameFilter={setNameFilter} setPage={setPage} />
            <RolesFilter
                rolesFilter={rolesFilter}
                setRolesFilter={setRolesFilter}
                setPage={setPage}
            />
            <Form.Group>
                <AlumniFilter
                    alumniFilter={alumniFilter}
                    setAlumniFilter={setAlumniFilter}
                    setPage={setPage}
                />
                <SuggestedForFilter
                    suggestedFilter={suggestedFilter}
                    setSuggestedFilter={setSuggestedFilter}
                    setPage={setPage}
                />
                <StudentCoachVolunteerFilter
                    studentCoachVolunteerFilter={studentCoachVolunteerFilter}
                    setStudentCoachVolunteerFilter={setStudentCoachVolunteerFilter}
                    setPage={setPage}
                />
                <ConfirmFilters
                    confirmFilter={confirmFilter}
                    setConfirmFilter={setConfirmFilter}
                    setPage={setPage}
                />
            </Form.Group>
            <StudentListLinebreak />
            <FilterControls>
                <ResetFiltersButton
                    setRolesFilter={setRolesFilter}
                    setNameFilter={setNameFilter}
                    setAlumniFilter={setAlumniFilter}
                    setSuggestedFilter={setSuggestedFilter}
                    setStudentCoachVolunteerFilter={setStudentCoachVolunteerFilter}
                    setConfirmFilter={setConfirmFilter}
                    setPage={setPage}
                />
            </FilterControls>
            {list}
        </StudentListSideMenu>
    );
}

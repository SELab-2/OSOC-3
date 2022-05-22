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

        setLoading(true);

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

            let tempStudents2: Student[];
            if (rolesFilter.length === 0) {
                tempStudents2 = tempStudents;
            } else {
                tempStudents2 = [];
                for (const student of tempStudents) {
                    let keep = false;
                    for (const skill of student.skills) {
                        for (const role of rolesFilter) {
                            if (role.value === skill.skillId) {
                                keep = true;
                            }
                        }
                    }
                    if (keep) {
                        tempStudents2.push(student);
                    }
                }
            }
            if (confirmFilter.length === 0) {
                setStudents(tempStudents2);
            } else {
                const finalStudents = [];
                for (const student of tempStudents2) {
                    let keep = false;
                    for (const status of confirmFilter) {
                        if (student.finalDecision === status.value) {
                            keep = true;
                        }
                    }
                    if (keep) {
                        finalStudents.push(student);
                    }
                }
                setStudents(finalStudents);
            }

            setMoreDataAvailable(false);
            setLoading(false);
            return;
        }

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
            } else {
                setMoreDataAvailable(true);
            }
            if (requestedPage === 0 || filterChanged) {
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
                if (requestedPage === 0) {
                    setAllStudents(response.students);
                } else {
                    setAllStudents(allStudents.concat(response.students));
                }
            }
            setPage(requestedPage + 1);
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
        getData(-1, false);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [nameFilter, rolesFilter, alumniFilter, studentCoachVolunteerFilter, confirmFilter]);

    useEffect(() => {
        refresh();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [params.editionId, suggestedFilter]);

    function refresh() {
        setStudents([]);
        setAllStudents([]);
        setPage(0);
        setAllDataFetched(false);
        setMoreDataAvailable(true);
        getData(-1, true);
    }

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
                />
                <StudentCoachVolunteerFilter
                    studentCoachVolunteerFilter={studentCoachVolunteerFilter}
                    setStudentCoachVolunteerFilter={setStudentCoachVolunteerFilter}
                    setPage={setPage}
                />
            </Form.Group>
            <ConfirmFilters
                confirmFilter={confirmFilter}
                setConfirmFilter={setConfirmFilter}
                setPage={setPage}
            />
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

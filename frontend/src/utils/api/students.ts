import axios from "axios";
import { Student, Students } from "../../data/interfaces/students";
import { axiosInstance } from "./api";
import { DropdownRole } from "../../components/StudentsComponents/StudentListFilters/RolesFilter/RolesFilter";

/**
 * API call to get students (and filter them).
 * @param edition The edition name.
 * @param nameFilter name to filter on.
 * @param rolesFilter roles to filter on.
 * @param alumniFilter check to filter on.
 * @param studentCoachVolunteerFilter check to filter on.
 * @param suggestedFilter check to filter on.
 * @param confirmFilter confirmation state to filter on.
 * @param page The page to fetch.
 * @param controller An optional AbortController to cancel the request
 */
export async function getStudents(
    edition: string,
    nameFilter: string,
    rolesFilter: DropdownRole[],
    alumniFilter: boolean,
    studentCoachVolunteerFilter: boolean,
    suggestedFilter: boolean,
    confirmFilter: DropdownRole[],
    page: number,
    controller: AbortController
): Promise<Students | null> {
    let rolesRequestField: string = "";

    for (const role of rolesFilter) {
        rolesRequestField += "skill_ids=" + role.value.toString() + "&";
    }
    let confirmRequestField: string = "";
    for (const confirmField of confirmFilter) {
        confirmRequestField += "decisions=" + confirmField.value.toString() + "&";
    }
    try {
        const response = await axiosInstance.get(
            "/editions/" +
                edition +
                "/students?name=" +
                nameFilter +
                "&alumni=" +
                alumniFilter +
                "&own_suggestions=" +
                suggestedFilter +
                "&" +
                rolesRequestField +
                "&student_coach=" +
                studentCoachVolunteerFilter +
                "&" +
                confirmRequestField +
                "&page=" +
                page,
            { signal: controller.signal }
        );
        return response.data as Students;
    } catch (error) {
        if (axios.isAxiosError(error) && error.code === "ERR_CANCELED") {
            return null;
        } else {
            throw error;
        }
    }
}

/**
 * API call to get a specific student.
 * @param edition The edition name.
 * @param studentId The ID of the student.
 */
export async function getStudent(edition: string, studentId: number): Promise<Student> {
    const request = "/editions/" + edition + "/students/" + studentId.toString();
    const response = await axiosInstance.get(request);
    return response.data.student as Student;
}

/**
 * API call to delete a student.
 * @param edition The edition name.
 * @param studentId The ID of the student that needs to be deleted.
 */
export async function removeStudent(edition: string, studentId: number): Promise<number> {
    try {
        const request = "/editions/" + edition + "/students/" + studentId.toString();
        await axiosInstance.delete(request);
        return 201;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return 422;
        } else {
            throw error;
        }
    }
}

/**
 * API call to make a suggestion on a student.
 * @param edition The edition name.
 * @param studentId The ID of the student on who a suggestion needs to be made.
 * @param suggestionArg The Suggestion value.
 * @param argumentationArg The argumentation for this suggestion.
 */
export async function makeSuggestion(
    edition: string,
    studentId: string,
    suggestionArg: number,
    argumentationArg: string
): Promise<number> {
    const request = "/editions/" + edition + "/students/" + studentId.toString() + "/suggestions";
    await axiosInstance.post(request, {
        suggestion: suggestionArg,
        argumentation: argumentationArg,
    });
    return 201;
}

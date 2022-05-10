import axios from "axios";
import { Student, Students } from "../../data/interfaces/students";
import { axiosInstance } from "./api";

export async function getStudents(
    edition: string,
    nameFilter: string,
    rolesFilter: number[],
    alumniFilter: boolean,
    studentCoachVolunteerFilter: boolean
): Promise<Students> {
    try {
        const response = await axiosInstance.get(
            "/editions/" +
                edition +
                "/students/?first_name=" +
                nameFilter +
                "&alumni=" +
                alumniFilter +
                "&student_coach=" +
                studentCoachVolunteerFilter
        );
        const students = response.data as Students;
        return students;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            throw error;
        } else {
            throw error;
        }
    }
}

export async function getStudent(edition: string, studentId: string): Promise<Student> {
    try {
        const request = "/editions/" + edition + "/students/" + studentId.toString();
        const response = await axiosInstance.get(request);
        const student = response.data.student as Student;
        console.log("get student");
        console.log(student);
        return student;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            throw error;
        } else {
            throw error;
        }
    }
}

export async function removeStudent(edition: string, studentId: string): Promise<number> {
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

export async function makeSuggestion(
    edition: string,
    studentId: string,
    suggestionArg: number,
    argumentationArg: string
): Promise<number> {
    try {
        const request =
            "/editions/" + edition + "/students/" + studentId.toString() + "/suggestions";
        await axiosInstance.post(request, {
            suggestion: suggestionArg,
            argumentation: argumentationArg,
        });
        return 201;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return 422;
        } else {
            throw error;
        }
    }
}

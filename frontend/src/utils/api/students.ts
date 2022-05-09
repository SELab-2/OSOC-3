import axios from "axios";
import {Student, Students} from "../../data/interfaces/students";
import { axiosInstance } from "./api";

export async function getStudents(edition: string, nameFilter: string, rolesFilter: number[], alumniFilter: boolean, studentCoachVolunteerFilter: boolean){
    try {
        const response = await axiosInstance.get("/editions/" + edition + "/students/?first_name=" + nameFilter + "&alumni=" + alumniFilter + "&student_coach=" + studentCoachVolunteerFilter);
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

export async function getStudent(edition: string, studentId: string){
    try {
        const request = "/editions/" + edition + "/students/" + studentId.toString()
        const response = await axiosInstance.get(request);
        const student = response.data.student as Student;
        return student;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            throw error;
        } else {
            throw error;
        }
    }
}

export async function removeStudent(edition: string, studentId: string){
    try {
        const request = "/editions/" + edition + "/students/" + studentId.toString()
        await axiosInstance.delete(request);
        return true;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return false;
        } else {
            throw error;
        }
    }
}

export async function makeSuggestion(edition: string, studentId: string, suggestionArg: number, argumentationArg: string){
    try {
        const request = "/editions/" + edition + "/students/" + studentId.toString() + "/suggestions"
        const response = await axiosInstance.post(request, { suggestion: suggestionArg, argumentation: argumentationArg });
        return response.status === 201;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return false;
        } else {
            throw error;
        }
    }
}
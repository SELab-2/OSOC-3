import axios from "axios";
import {Student, Students} from "../../data/interfaces/students";
import { axiosInstance } from "./api";

export async function getStudents(edition: string, nameFilter: string, rolesFilter: number[], alumniFilter: boolean, studentCoachVolunteerFilter: boolean){
    try {
        console.log(nameFilter)
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
        console.log(response.data)
        const student = response.data as Student;
        return student;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            throw error;
        } else {
            throw error;
        }
    }
}

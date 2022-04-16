import axios from "axios";
import { axiosInstance } from "./api";

export async function getProjects(edition: string) {
    try {
        const response = await axiosInstance.get("/editions/" + edition + "/projects/");
        const projects = response.data;
        return projects;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return false;
        } else {
            throw error;
        }
    }
}

export async function getProject(edition: string, projectId: number) {
    try {
        const response = await axiosInstance.get("/editions/" + edition + "/projects/" + projectId);
        const project = response.data;
        return project;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return false;
        } else {
            throw error;
        }
    }
}

export async function deleteProject(edition: string, projectId: number) {
    try {
        const response = await axiosInstance.delete(
            "/editions/" + edition + "/projects/" + projectId
        );
        console.log(response);
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return false;
        } else {
            throw error;
        }
    }
}

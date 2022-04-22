import axios from "axios";
import { Projects, Project } from "../../data/interfaces/projects";
import { axiosInstance } from "./api";

export async function getProjects(edition: string, page: number) {
    try {
        const response = await axiosInstance.get("/editions/" + edition + "/projects?page=" + page.toString());
        const projects = response.data as Projects;
        return projects;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return null;
        } else {
            throw error;
        }
    }
}

export async function getProject(edition: string, projectId: number) {
    try {
        const response = await axiosInstance.get("/editions/" + edition + "/projects/" + projectId);
        const project = response.data as Project;
        return project;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return null;
        } else {
            throw error;
        }
    }
}

export async function deleteProject(edition: string, projectId: number) {
    try {
        await axiosInstance.delete("/editions/" + edition + "/projects/" + projectId);
        return true;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return false;
        } else {
            throw error;
        }
    }
}

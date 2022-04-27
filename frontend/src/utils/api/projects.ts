import axios from "axios";
import { Projects, Project, CreateProject } from "../../data/interfaces/projects";
import { axiosInstance } from "./api";

export async function getProjects(
    edition: string,
    name: string,
    ownProjects: boolean,
    page: number
): Promise<Projects | null> {
    try {
        const response = await axiosInstance.get(
            "/editions/" +
                edition +
                "/projects/?name=" +
                name +
                "&coach=" +
                ownProjects.toString() +
                "&page=" +
                page.toString()
        );
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

export async function getProject(edition: string, projectId: number): Promise<Project | null> {
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

export async function createProject(
    edition: string,
    name: string,
    numberOfStudents: number,
    skills: string[],
    partners: string[],
    coaches: string[]
) {
    const payload: CreateProject = {
        name: name,
        number_of_students: numberOfStudents,
        skills: skills,
        partners: partners,
        coaches: coaches,
    };

    try {
        const response = await axiosInstance.post("editions/" + edition + "/projects/", payload);
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

export async function deleteProject(edition: string, projectId: number): Promise<boolean> {
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

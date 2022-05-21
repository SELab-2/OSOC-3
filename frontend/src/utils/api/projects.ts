import axios from "axios";
import { CreateProject, Project, Projects } from "../../data/interfaces/projects";
import { axiosInstance } from "./api";

/**
 * API call to get projects (and filter them)
 * @param edition The edition name.
 * @param name To filter on project name.
 * @param ownProjects To filter on your own projects.
 * @param page The requested page.
 * @param controller An optional AbortController to cancel the request
 */
export async function getProjects(
    edition: string,
    name: string,
    ownProjects: boolean,
    page: number,
    controller: AbortController
): Promise<Projects | null> {
    try {
        const response = await axiosInstance.get(
            "/editions/" +
                edition +
                "/projects?name=" +
                name +
                "&coach=" +
                ownProjects.toString() +
                "&page=" +
                page.toString(),
            { signal: controller.signal }
        );
        return response.data as Projects;
    } catch (error) {
        if (axios.isAxiosError(error) && error.code === "ERR_CANCELED") {
            return null;
        } else {
            throw error;
        }
    }
}

/**
 * API call to get a specific project.
 * @param edition The edition name.
 * @param projectId The ID of the project.
 * @returns A Project object when successful.
 */
export async function getProject(edition: string, projectId: number): Promise<Project | null> {
    try {
        const response = await axiosInstance.get("/editions/" + edition + "/projects/" + projectId);
        return response.data as Project;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return null;
        } else {
            throw error;
        }
    }
}

/**
 * API call to create a project.
 * @param edition The edition name.
 * @param name The name of the new project.
 * @param numberOfStudents The amount of students needed for this project.
 * @param skills The skills that are needed for this project.
 * @param partners The partners of the project.
 * @param coaches The coaches that will coach the project.
 * @returns The newly created object.
 */
export async function createProject(
    edition: string,
    name: string,
    numberOfStudents: number,
    skills: string[],
    partners: string[],
    coaches: number[]
): Promise<Project | null> {
    const payload: CreateProject = {
        name: name,
        number_of_students: numberOfStudents,
        skills: skills,
        partners: partners,
        coaches: coaches,
    };

    try {
        const response = await axiosInstance.post("editions/" + edition + "/projects/", payload);
        return response.data as Project;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return null;
        } else {
            throw error;
        }
    }
}

/**
 * API call to delete a project.
 * @param edition The edition name.
 * @param projectId The ID of the project that needs to be deleted.
 * @returns true if the deletion was successful or false if it failed.
 */
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

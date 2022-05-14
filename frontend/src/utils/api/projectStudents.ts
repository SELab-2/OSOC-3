import axios from "axios";
import { axiosInstance } from "./api";
import { AddRoleSuggestion } from "../../data/interfaces/projects";

/**
 * API call to make a student role suggestion.
 * @param edition The edition name.
 * @param projectId The projectId where to add the suggestion.
 * @param projectRoleId The id of the project role.
 * @param studentId The id of the student to add.
 * @param argumentation Why this student is a good fit.
 * @returns if the suggestion was created successfully.
 */
export async function addStudentToProject(
    edition: string,
    projectId: string,
    projectRoleId: string,
    studentId: string,
    argumentation: string | undefined
): Promise<boolean> {
    const payload: AddRoleSuggestion = {
        argumentation: argumentation || "",
    };

    try {
        const response = await axiosInstance.post(
            "editions/" +
                edition +
                "/projects/" +
                projectId +
                "/roles/" +
                projectRoleId +
                "/students/" +
                studentId,
            payload
        );
        if (response) return true;
        else return false;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return false;
        } else {
            throw error;
        }
    }
}

/**
 * API call to change a student role suggestion.
 * @param edition The edition name.
 * @param projectId The projectId where to add the suggestion.
 * @param projectRoleId The id of the project role.
 * @param studentId The id of the student to add.
 * @param argumentation The updated argumentation why this student is a good fit.
 * @returns if the suggestion was updated successfully.
 */
export async function patchStudentProjectRole(
    edition: string,
    projectId: string,
    projectRoleId: string,
    studentId: string,
    argumentation: string | undefined
): Promise<boolean> {
    const payload: AddRoleSuggestion = {
        argumentation: argumentation || "",
    };

    try {
        const response = await axiosInstance.patch(
            "editions/" +
                edition +
                "/projects/" +
                projectId +
                "/roles/" +
                projectRoleId +
                "/students/" +
                studentId,
            payload
        );
        if (response) return true;
        else return false;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return false;
        } else {
            throw error;
        }
    }
}

/**
 * API call to delete a student from a project role.
 * @param edition The edition name.
 * @param projectId The ID of the project.
 * @param projectRoleId The id of the project role.
 * @param studentId The id of the student to remove from the project role.
 * @returns true if the deletion was successful or false if it failed.
 */
export async function deleteStudentFromProject(
    edition: string,
    projectId: string,
    projectRoleId: string,
    studentId: string
): Promise<boolean> {
    try {
        await axiosInstance.delete(
            "editions/" +
                edition +
                "/projects/" +
                projectId +
                "/roles/" +
                projectRoleId +
                "/students/" +
                studentId
        );
        return true;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return false;
        } else {
            throw error;
        }
    }
}

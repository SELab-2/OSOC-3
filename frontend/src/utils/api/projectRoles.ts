import axios from "axios";
import { axiosInstance } from "./api";
import { CreateProjectRole, ProjectRole } from "../../data/interfaces/projects";

/**
 * API call to get all project roles of a project.
 * @param edition The edition name.
 * @param projectId The projectId where to add the new project role.
 * @returns A list of the project roles.
 */
export async function getProjectRoles(
    edition: string,
    projectId: string
): Promise<ProjectRole[] | null> {
    try {
        const response = await axiosInstance.get(
            "editions/" + edition + "/projects/" + projectId + "/roles"
        );
        const projectRole = response.data as ProjectRole[];

        return projectRole;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return null;
        } else {
            throw error;
        }
    }
}

/**
 * API call to create a ProjectRole.
 * @param edition The edition name.
 * @param projectId The projectId where to add the new project role.
 * @param skillId The id of the skill.
 * @param description Optional description for this skill.
 * @param slots The number of places for this skill.
 * @returns The newly created project role object.
 */
export async function createProjectRole(
    edition: string,
    projectId: string,
    skillId: number,
    description: string | undefined,
    slots: number
): Promise<ProjectRole | null> {
    const payload: CreateProjectRole = {
        skill_id: skillId,
        description: description || "",
        slots: slots,
    };

    try {
        const response = await axiosInstance.post(
            "editions/" + edition + "/projects/" + projectId + "/roles",
            payload
        );
        const projectRole = response.data as ProjectRole;

        return projectRole;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return null;
        } else {
            throw error;
        }
    }
}

/**
 * API call to edit a ProjectRole.
 * @param edition The edition name.
 * @param projectRoleId The id of the project role.
 * @param projectId The projectId where to change the project role.
 * @param skillId The id of the skill.
 * @param description Optional new description for this skill.
 * @param slots The new number of places for this skill.
 * @returns The updated project role object.
 */
export async function editProjectRole(
    edition: string,
    projectRoleId: string,
    projectId: string,
    skillId: number,
    description: string | undefined,
    slots: number
): Promise<ProjectRole | null> {
    const payload: CreateProjectRole = {
        skill_id: skillId,
        description: description || "",
        slots: slots,
    };

    try {
        const response = await axiosInstance.patch(
            "editions/" + edition + "/projects/" + projectId + "/roles/" + projectRoleId,
            payload
        );
        const projectRole = response.data as ProjectRole;

        return projectRole;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return null;
        } else {
            throw error;
        }
    }
}

/**
 * API call to delete a project role
 * @param edition The edition name.
 * @param projectId The projectId where to delete a project role.
 * @param projectRoleId The Id of the project role to delete
 * @returns whether the delete was successful or not.
 */
export async function deleteProjectRole(
    edition: string,
    projectId: string,
    projectRoleId: string
): Promise<boolean> {
    try {
        await axiosInstance.delete(
            "editions/" + edition + "/projects/" + projectId + "/roles/" + projectRoleId
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

import axios from "axios";
import { axiosInstance } from "./api";
import { CreateProjectRole, ProjectRole } from "../../data/interfaces/projects";

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

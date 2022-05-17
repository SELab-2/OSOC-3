import axios from "axios";
import { axiosInstance } from "./api";
import { CreateSkill, Skill, Skills } from "../../data/interfaces/skills";

/**
 * API call to get skills
 * @returns a list of skills
 */
export async function getSkills(): Promise<Skills | null> {
    try {
        const response = await axiosInstance.get("skills");
        const skills = response.data as Skills;
        return skills;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return null;
        } else {
            throw error;
        }
    }
}

/**
 * API call to create a Skill.
 * @param name The skill name.
 * @returns The newly created project role object.
 */
export async function createSkill(name: string): Promise<Skill | null> {
    const payload: CreateSkill = {
        name: name,
    };

    try {
        const response = await axiosInstance.post("skills", payload);
        const skill = response.data as Skill;
        return skill;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return null;
        } else {
            throw error;
        }
    }
}

/**
 * API call to delete a Skill.
 * @param skillId The skill id.
 * @returns True if the delete was successful, false if it failed.
 */
export async function deleteSkill(skillId: string): Promise<boolean> {
    try {
        await axiosInstance.delete("skills/" + skillId);
        return true;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return false;
        } else {
            throw error;
        }
    }
}

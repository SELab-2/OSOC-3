/**
 * Data about a skill
 */
export interface Skill {
    /** The id of the skill */
    skillId: number;

    /** The name of the skill */
    name: string;
}

/**
 * To create a skill
 */
export interface CreateSkill {
    /** The name of the skill */
    name: string;
}

/**
 * A list of skills
 */
export interface Skills {
    /** The list of skills */
    skills: Skill[];
}

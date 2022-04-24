import { SkillProject } from "../../../../../data/interfaces/projects";
import { Input, AddButton } from "../../styles";

export default function Skill({
    skill,
    setSkill,
    skills,
    setSkills,
}: {
    skill: string;
    setSkill: (skill: string) => void;
    skills: SkillProject[];
    setSkills: (skills: SkillProject[]) => void;
}) {
    const availableSkills = ["Frontend", "Backend", "Database", "Design"];

    return (
        <div>
            <Input
                value={skill}
                onChange={e => setSkill(e.target.value)}
                placeholder="Skill"
                list="skills"
            />
            <datalist id="skills">
                {availableSkills.map((availableCoach, _index) => {
                    return <option key={_index} value={availableCoach} />;
                })}
            </datalist>

            <AddButton
                onClick={() => {
                    
                    if (availableSkills.some(availableSkill => availableSkill === skill)) {
                        if (!skills.some(existingSkill => existingSkill.skill === skill)) {
                            const newSkills = [...skills];
                            const newSkill: SkillProject = {
                                skill: skill,
                                description: undefined,
                                amount: undefined,
                            };
                            newSkills.push(newSkill);
                            setSkills(newSkills);
                        }
                    }
                }}
            >
                Add skill
            </AddButton>
        </div>
    );
}

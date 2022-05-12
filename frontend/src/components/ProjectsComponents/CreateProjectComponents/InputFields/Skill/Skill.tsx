import { useEffect, useState } from "react";
import { SkillProject, Skill } from "../../../../../data/interfaces/projects";
import { getSkills } from "../../../../../utils/api/projectRoles";
import { Input, AddButton } from "../../styles";

export default function SkillInput({
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
    const [availableSkills, setAvailableSkills] = useState<Skill[]>([]);

    useEffect(() => {
        async function callCoaches() {
            setAvailableSkills((await getSkills()) || []);
        }
        callCoaches();
    }, []);

    return (
        <div>
            <Input
                value={skill}
                onChange={e => setSkill(e.target.value)}
                onKeyDown={e => {
                    if (e.key === "Enter") addSkill();
                }}
                placeholder="Skill"
                list="skills"
            />
            <datalist id="skills">
                {availableSkills.map((availableSkill, _index) => {
                    return <option key={availableSkill.skillId} value={availableSkill.name} />;
                })}
            </datalist>

            <AddButton onClick={addSkill}>Add</AddButton>
        </div>
    );

    function addSkill() {
        let skillToAdd: Skill | undefined;
        availableSkills.forEach(availableSkill => {
            if (availableSkill.name === skill) {
                skillToAdd = availableSkill;
            }
        });
        if (skillToAdd) {
            const newSkills = [...skills];
            const newSkill: SkillProject = {
                skill: skillToAdd,
                description: "",
                slots: 1,
            };
            newSkills.push(newSkill);
            setSkills(newSkills);
        }
        setSkill("");
    }
}

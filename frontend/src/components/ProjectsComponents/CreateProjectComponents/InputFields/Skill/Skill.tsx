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
                onKeyDown={e => {
                    if (e.key === "Enter") addSkill();
                }}
                placeholder="Skill"
                list="skills"
            />
            <datalist id="skills">
                {availableSkills.map((availableCoach, _index) => {
                    return <option key={_index} value={availableCoach} />;
                })}
            </datalist>

            <AddButton onClick={addSkill}>Add</AddButton>
        </div>
    );

    function addSkill() {
        if (availableSkills.some(availableSkill => availableSkill === skill)) {
            const newSkills = [...skills];
            const newSkill: SkillProject = {
                skill: skill,
                description: "",
                amount: 1,
            };
            newSkills.push(newSkill);
            setSkills(newSkills);
        }
        setSkill("");
    }
}

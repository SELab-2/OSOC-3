import { Input, AddButton } from "../../styles";

export default function Skill({
    skills,
    setSkills,
}: {
    skills: string[];
    setSkills: (skills: string[]) => void;
}) {
    return (
        <div>
            <Input value={skills} onChange={e => setSkills([])} placeholder="Skill" />
            <AddButton>Add skill</AddButton>
        </div>
    );
}

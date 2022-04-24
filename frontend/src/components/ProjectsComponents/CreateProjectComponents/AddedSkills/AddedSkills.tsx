import { SkillProject } from "../../../../data/interfaces/projects";

export default function AddedSkills({
    skills,
    setSkills,
}: {
    skills: SkillProject[];
    setSkills: (skills: SkillProject[]) => void;
}) {
    return (
        <div>
            {skills.map((skill, _index) => (
                <div key={_index}>
                    {skill.skill}
                    <input
                        type="number"
                        value={skill.amount}
                        placeholder="Amount"
                        min={1}
                        onChange={event => {
                            const newList = skills.map((item, otherIndex) => {
                                if (_index === otherIndex) {
                                    const updatedItem = {
                                        ...item,
                                        amount: event.target.valueAsNumber,
                                    };
                                    return updatedItem;
                                }
                                return item;
                            });

                            setSkills(newList);
                        }}
                    />
                    <input
                        type="text"
                        value={skill.description}
                        placeholder="Description"
                        onChange={event => {
                            const newList = skills.map((item, otherIndex) => {
                                if (_index === otherIndex) {
                                    const updatedItem = {
                                        ...item,
                                        description: event.target.value,
                                    };
                                    return updatedItem;
                                }
                                return item;
                            });

                            setSkills(newList);
                        }}
                    />
                </div>
            ))}
        </div>
    );
}

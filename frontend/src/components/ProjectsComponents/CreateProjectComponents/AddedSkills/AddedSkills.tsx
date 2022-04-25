import { SkillProject } from "../../../../data/interfaces/projects";
import { Input } from "../styles";
import { AmountInput, SkillContainer, DescriptionContainer, Delete, TopContainer } from "./styles";
import { TiDeleteOutline } from "react-icons/ti";

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
                <SkillContainer key={_index}>
                    <TopContainer>
                        {skill.skill}
                        <AmountInput
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
                        <Delete>
                            <TiDeleteOutline size={"20px"} />
                        </Delete>
                    </TopContainer>
                    <DescriptionContainer>
                        <Input
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
                    </DescriptionContainer>
                </SkillContainer>
            ))}
        </div>
    );
}

import { SkillProject } from "../../../../data/interfaces/projects";
import {
    AmountInput,
    SkillContainer,
    DescriptionContainer,
    Delete,
    TopContainer,
    SkillName,
    TopLeftContainer,
    DescriptionInput,
} from "./styles";
import { TiDeleteOutline } from "react-icons/ti";
import React from "react";

/**
 * 
 * @param skills the state of the added skills
 * @param setSkills used to update the added skills and there attributes

 * @returns a react component of all the added skills
 */
export default function AddedSkills({
    skills,
    setSkills,
}: {
    skills: SkillProject[];
    setSkills: (skills: SkillProject[]) => void;
}) {
    /**
     * This function is called when an input field is changed.
     * @param event a react event
     * @param index the index of the skill to change
     * @param amount whether to update the amount (true) or to update the description (false)
     */
    function updateSkills(
        event: React.ChangeEvent<HTMLInputElement>,
        index: number,
        amount: boolean
    ) {
        const newList = skills.map((item, otherIndex) => {
            if (index === otherIndex) {
                if (amount) {
                    if (event.target.valueAsNumber < 1) return item;
                    return {
                        ...item,
                        slots: event.target.valueAsNumber,
                    };
                }
                return {
                    ...item,
                    description: event.target.value,
                };
            }
            return item;
        });
        setSkills(newList);
    }

    return (
        <div>
            {skills.map((skill, index) => (
                <SkillContainer key={index}>
                    <TopContainer>
                        <TopLeftContainer>
                            <SkillName>{skill.skill.name}</SkillName>

                            <AmountInput
                                type="number"
                                value={skill.slots.toString()}
                                placeholder="Amount"
                                min={1}
                                onChange={event => {
                                    updateSkills(event, index, true);
                                }}
                            />
                        </TopLeftContainer>
                        <Delete
                            onClick={() => {
                                const newSkills = [...skills];
                                newSkills.splice(index, 1);
                                setSkills(newSkills);
                            }}
                        >
                            <TiDeleteOutline size={"20px"} />
                        </Delete>
                    </TopContainer>

                    <DescriptionContainer>
                        <DescriptionInput
                            type="text"
                            value={skill.description}
                            placeholder="Description"
                            onChange={event => {
                                updateSkills(event, index, false);
                            }}
                        />
                    </DescriptionContainer>
                </SkillContainer>
            ))}
        </div>
    );
}

import { useEffect, useState } from "react";
import { Skill } from "../../../../data/interfaces/skills";
import { getSkills } from "../../../../utils/api/skills";
import { CreateButton } from "../../../Common/Buttons";
import { AddNewSkillContainer, NewSkill, StyledFormSelect } from "./styles";

export default function AddNewSkill() {
    const [addingSkill, setAddingSkill] = useState(false);

    const [availableSkills, setAvailableSkills] = useState<Skill[]>([]);

    useEffect(() => {
        async function callSkills() {
            setAvailableSkills((await getSkills())?.skills || []);
        }
        callSkills();
    }, []);

    return (
        <>
            {!addingSkill ? (
                <AddNewSkillContainer>
                    <CreateButton label="Add new skill" onClick={() => setAddingSkill(true)} />
                </AddNewSkillContainer>
            ) : (
                <NewSkill>
                    <StyledFormSelect>
                        {availableSkills.map(skill => (
                            <option>{skill.name}</option>
                        ))}
                    </StyledFormSelect>
                </NewSkill>
            )}
        </>
    );
}

import { useEffect, useState } from "react";
import { CreateProjectRole } from "../../../../data/interfaces/projects";
import { Skill } from "../../../../data/interfaces/skills";
import { getSkills } from "../../../../utils/api/skills";
import { CreateButton } from "../../../Common/Buttons";
import { StyledFormControl } from "../../../Common/Forms/styles";
import { AmountInput } from "../../../ProjectsComponents/CreateProjectComponents/AddedSkills/styles";
import { AddNewSkillContainer, NewSkill } from "./styles";

export default function AddNewSkill() {
    const [addingSkill, setAddingSkill] = useState(false);

    const [availableSkills, setAvailableSkills] = useState<Skill[]>([]);

    const [projectRole, setProjectRole] = useState<CreateProjectRole>();
    const [chosenSkill, setChosenSkill] = useState<Skill>();

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
                    <StyledFormControl
                        as="select"
                        value={chosenSkill?.name}
                        onChange={(e: { target: { value: string } }) => {
                            let skillToAdd: Skill | undefined;
                            availableSkills.forEach(availableSkill => {
                                if (availableSkill.name === e.target.value) {
                                    skillToAdd = availableSkill;
                                }
                            });
                            if (skillToAdd) setChosenSkill(skillToAdd);
                        }}
                    >
                        {availableSkills.map(skill => (
                            <option value={skill.name}>{skill.name}</option>
                        ))}
                    </StyledFormControl>
                    <AmountInput
                        type="number"
                        value={projectRole?.slots}
                        placeholder="Amount"
                        min={1}
                        onChange={event => {
                            setProjectRole(undefined);
                        }}
                    />
                    {projectRole && projectRole.slots === 1 ? (
                        <div>student</div>
                    ) : (
                        <div>students</div>
                    )}
                </NewSkill>
            )}
        </>
    );
}

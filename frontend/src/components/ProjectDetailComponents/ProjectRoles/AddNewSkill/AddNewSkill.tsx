import { ChangeEvent, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { toast } from "react-toastify";
import { Skill } from "../../../../data/interfaces/skills";
import { createProjectRole } from "../../../../utils/api/projectRoles";
import { getSkills } from "../../../../utils/api/skills";
import { CancelButton } from "../../../../views/CreateEditionPage/styles";
import { CreateButton } from "../../../Common/Buttons";
import { DescriptionInput } from "../../../ProjectsComponents/CreateProjectComponents/AddedSkills/styles";
import {
    AddNewSkillContainer,
    NewSkill,
    StyledFormSelect,
    AmountInput,
    AddNewSkillButton,
    NewSkillLeft,
    NewSKillRight,
    NewSkillTop,
    NewSkillBottom,
} from "./styles";

export default function AddNewSkill({
    setGotProject,
}: {
    setGotProject: (value: boolean) => void;
}) {
    const [addingSkill, setAddingSkill] = useState(false);

    const [availableSkills, setAvailableSkills] = useState<Skill[]>([]);

    const [slots, setSlots] = useState(1);
    const [chosenSkill, setChosenSkill] = useState<Skill>();
    const [description, setDescription] = useState("");

    const params = useParams();
    const editionId = params.editionId!;
    const projectId = params.projectId!;

    useEffect(() => {
        async function callSkills() {
            setAvailableSkills((await getSkills())?.skills || []);
            setChosenSkill((await getSkills())?.skills[0]);
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
                    <NewSkillTop>
                        <NewSkillLeft>
                            <StyledFormSelect
                                value={chosenSkill?.name}
                                as="select"
                                onChange={(e: ChangeEvent<HTMLSelectElement>) => {
                                    let skillToAdd: Skill | undefined;
                                    availableSkills.forEach(availableSkill => {
                                        if (availableSkill.name === e.target.value) {
                                            skillToAdd = availableSkill;
                                        }
                                    });
                                    if (skillToAdd) {
                                        setChosenSkill(skillToAdd);
                                    }
                                }}
                            >
                                {availableSkills.map(skill => (
                                    <option key={skill.skillId} value={skill.name}>
                                        {skill.name}
                                    </option>
                                ))}
                            </StyledFormSelect>
                            <AmountInput
                                type="number"
                                value={slots.toString()}
                                placeholder="Amount"
                                min={1}
                                onChange={event => {
                                    setSlots(event.target.valueAsNumber);
                                }}
                            />
                            {slots === 1 ? <div>student</div> : <div>students</div>}
                        </NewSkillLeft>
                        <NewSKillRight>
                            <AddNewSkillButton
                                label="Add skill"
                                onClick={() => {
                                    addSkillToProject();
                                }}
                            />
                            <CancelButton onClick={() => setAddingSkill(false)}>
                                Cancel
                            </CancelButton>
                        </NewSKillRight>
                    </NewSkillTop>
                    <NewSkillBottom>
                        <DescriptionInput
                            type="text"
                            value={description}
                            placeholder="Description"
                            onChange={event => {
                                setDescription(event.target.value);
                            }}
                        />
                    </NewSkillBottom>
                </NewSkill>
            )}
        </>
    );

    async function addSkillToProject() {
        if (chosenSkill) {
            await toast.promise(
                createProjectRole(
                    editionId,
                    projectId.toString(),
                    chosenSkill.skillId,
                    description,
                    slots
                ),
                {
                    pending: "Adding skill",
                    success: "Successfully added skill",
                    error: "Something went wrong",
                }
            );
            setGotProject(false);
            setAddingSkill(false);
        }
    }
}

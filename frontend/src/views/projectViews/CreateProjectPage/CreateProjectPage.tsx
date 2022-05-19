import {
    CreateProjectContainer,
    Label,
    CenterContainer,
    Center,
    CancelButton,
    CenterTitle,
} from "./styles";
import { createProject } from "../../../utils/api/projects";
import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { BiArrowBack } from "react-icons/bi";
import {
    NameInput,
    CoachInput,
    SkillInput,
    PartnerInput,
    AddedCoaches,
    AddedPartners,
    AddedSkills,
} from "../../../components/ProjectsComponents/CreateProjectComponents";
import { SkillProject } from "../../../data/interfaces/projects";
import { User } from "../../../utils/api/users/users";
import { toast } from "react-toastify";
import { createProjectRole } from "../../../utils/api/projectRoles";
import { CreateButton } from "../../../components/Common/Buttons";
import InfoUrl from "../../../components/ProjectsComponents/CreateProjectComponents/InputFields/InfoUrl";
/**
 * React component of the create project page.
 * @returns The create project page.
 */

export default function CreateProjectPage() {
    const [name, setName] = useState(""); // State for project name

    const [infoUrl, setInfoUrl] = useState(""); // State for info link

    const [coach, setCoach] = useState("");
    const [coaches, setCoaches] = useState<User[]>([]); // States for coaches

    const [skill, setSkill] = useState("");
    const [projectSkills, setProjectSkills] = useState<SkillProject[]>([]); // States for skills

    const [partner, setPartner] = useState("");
    const [partners, setPartners] = useState<string[]>([]); // States for partners

    const navigate = useNavigate();
    const params = useParams();
    const editionId = params.editionId!;

    return (
        <CenterContainer>
            <CreateProjectContainer>
                <CenterTitle>
                    <h2>New Project</h2>
                </CenterTitle>
                <Label>Name</Label>
                <NameInput name={name} setName={setName} />

                <Label>Info Link</Label>
                <InfoUrl infoUrl={infoUrl} setInfoUrl={setInfoUrl} />

                <Label>Add Coaches</Label>
                <CoachInput
                    coach={coach}
                    setCoach={setCoach}
                    coaches={coaches}
                    setCoaches={setCoaches}
                />
                <AddedCoaches coaches={coaches} setCoaches={setCoaches} />

                <Label>Add Skills</Label>
                <SkillInput
                    skill={skill}
                    setSkill={setSkill}
                    skills={projectSkills}
                    setSkills={setProjectSkills}
                />
                <AddedSkills skills={projectSkills} setSkills={setProjectSkills} />

                <Label>Add Partners</Label>
                <PartnerInput
                    partner={partner}
                    setPartner={setPartner}
                    partners={partners}
                    setPartners={setPartners}
                />
                <AddedPartners items={partners} setItems={setPartners} />
                <Center>
                    <CancelButton onClick={() => navigate("/editions/" + editionId + "/projects/")}>
                        <BiArrowBack />
                        Cancel
                    </CancelButton>
                    <CreateButton label="Create Project" onClick={makeProject} />
                </Center>
            </CreateProjectContainer>
        </CenterContainer>
    );

    async function makeProject() {
        if (name === "") {
            toast.error("Project name must be filled in", {
                toastId: "createProjectNoName",
            });
            return;
        }

        let badSkill = false;
        projectSkills.forEach(projectSkill => {
            if (isNaN(projectSkill.slots)) {
                badSkill = true;
                toast.error(projectSkill.skill.name + " is missing the amount of students", {
                    toastId: "invalidSkill" + projectSkill.skill.name,
                });
            }
        });
        if (badSkill) return;

        const coachIds: number[] = [];
        coaches.forEach(coachToAdd => {
            coachIds.push(coachToAdd.userId);
        });
        const response = await createProject(editionId, name, infoUrl, partners, coachIds);

        if (response) {
            await toast.promise(addProjectRoles(response.projectId), {
                pending: "Creating project",
                success: "Successfully created project",
                error: "Something went wrong",
            });
            navigate("/editions/" + editionId + "/projects/" + response.projectId);
        } else toast.error("Something went wrong");
    }

    async function addProjectRoles(projectId: number) {
        // Use a for loop or else await won't work as intended
        for (const projectSkill of projectSkills) {
            const addedSkill = await createProjectRole(
                editionId,
                projectId.toString(),
                projectSkill.skill.skillId,
                projectSkill.description,
                projectSkill.slots
            );
            if (!addedSkill) toast.error("Couldn't add skill" + projectSkill.skill.name);
        }
    }
}

import {
    CreateProjectContainer,
    CreateButton,
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
    NumberOfStudentsInput,
    CoachInput,
    SkillInput,
    PartnerInput,
    AddedCoaches,
    AddedPartners,
    AddedSkills,
} from "../../../components/ProjectsComponents/CreateProjectComponents";
import { SkillProject } from "../../../data/interfaces/projects";
import { User } from "../../../utils/api/users/users";

/**
 * React component of the create project page.
 * @returns The create project page.
 */
export default function CreateProjectPage() {
    const [name, setName] = useState("");
    const [numberOfStudents, setNumberOfStudents] = useState<number>(1);

    // States for coaches
    const [coach, setCoach] = useState("");
    const [coaches, setCoaches] = useState<User[]>([]);

    // States for skills
    const [skill, setSkill] = useState("");
    const [skills, setSkills] = useState<SkillProject[]>([]);

    // States for partners
    const [partner, setPartner] = useState("");
    const [partners, setPartners] = useState<string[]>([]);

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

                <Label>Number of students</Label>
                <NumberOfStudentsInput
                    numberOfStudents={numberOfStudents}
                    setNumberOfStudents={setNumberOfStudents}
                />

                <Label>Coaches</Label>
                <CoachInput
                    coach={coach}
                    setCoach={setCoach}
                    coaches={coaches}
                    setCoaches={setCoaches}
                />
                <AddedCoaches coaches={coaches} setCoaches={setCoaches} />

                <Label>Skills</Label>
                <SkillInput
                    skill={skill}
                    setSkill={setSkill}
                    skills={skills}
                    setSkills={setSkills}
                />
                <AddedSkills skills={skills} setSkills={setSkills} />

                <Label>Partners</Label>
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
                    <CreateButton
                        onClick={async () => {
                            if (name === "") {
                                alert("Project name must be filled in");
                                return;
                            }

                            if (isNaN(numberOfStudents)) {
                                alert("Number of students must be filled in");
                                return;
                            }

                            const coachIds: number[] = [];
                            coaches.forEach(coachToAdd => {
                                coachIds.push(coachToAdd.userId);
                            });

                            const response = await createProject(
                                editionId,
                                name,
                                numberOfStudents!,
                                [], // Empty skills for now TODO
                                partners,
                                coachIds
                            );
                            if (response) {
                                navigate(
                                    "/editions/" + editionId + "/projects/" + response.projectId
                                );
                            } else alert("Something went wrong :(");
                        }}
                    >
                        Create Project
                    </CreateButton>
                </Center>
            </CreateProjectContainer>
        </CenterContainer>
    );
}

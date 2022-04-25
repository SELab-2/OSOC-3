import { CreateProjectContainer, CreateButton, Label } from "./styles";
import { createProject } from "../../../utils/api/projects";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { GoBack } from "../ProjectDetailPage/styles";
import { BiArrowBack } from "react-icons/bi";
import {
    NameInput,
    NumberOfStudentsInput,
    CoachInput,
    SkillInput,
    PartnerInput,
    AddedItems,
    AddedSkills,
} from "../../../components/ProjectsComponents/CreateProjectComponents";
import { SkillProject } from "../../../data/interfaces/projects";

export default function CreateProjectPage() {
    const [name, setName] = useState("");
    const [numberOfStudents, setNumberOfStudents] = useState<number>(0);

    // States for coaches
    const [coach, setCoach] = useState("");
    const [coaches, setCoaches] = useState<string[]>([]);

    // States for skills
    const [skill, setSkill] = useState("");
    const [skills, setSkills] = useState<SkillProject[]>([]);

    // States for partners
    const [partner, setPartner] = useState("");
    const [partners, setPartners] = useState<string[]>([]);

    const navigate = useNavigate();

    return (
        <CreateProjectContainer>
            <GoBack onClick={() => navigate("/editions/2022/projects/")}>
                <BiArrowBack />
                Cancel
            </GoBack>
            <h2>New Project</h2>

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
            <AddedItems items={coaches} setItems={setCoaches} />

            <Label>Skills</Label>
            <SkillInput skill={skill} setSkill={setSkill} skills={skills} setSkills={setSkills} />
            <AddedSkills skills={skills} setSkills={setSkills} />

            <Label>Partners</Label>
            <PartnerInput
                partner={partner}
                setPartner={setPartner}
                partners={partners}
                setPartners={setPartners}
            />
            <AddedItems items={partners} setItems={setPartners} />

            <CreateButton
                onClick={async () => {
                    const response = await createProject(
                        "2022",
                        name,
                        numberOfStudents!,
                        [],
                        partners,
                        coaches
                    );
                    if (response) {
                        navigate("/editions/2022/projects/");
                    } else alert("Something went wrong :(");
                }}
            >
                Create Project
            </CreateButton>
        </CreateProjectContainer>
    );
}

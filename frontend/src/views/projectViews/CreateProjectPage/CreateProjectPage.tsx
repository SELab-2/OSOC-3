import { CreateProjectContainer, CreateButton } from "./styles";
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
    AddedCoaches,
} from "../../../components/ProjectsComponents/CreateProjectComponents";

export default function CreateProjectPage() {
    const [name, setName] = useState("");
    const [numberOfStudents, setNumberOfStudents] = useState<number>(0);
    const [skills, setSkills] = useState<string[]>([]);
    const [partners, setPartners] = useState<string[]>([]);

    // States for coaches
    const [coach, setCoach] = useState("");
    const [coaches, setCoaches] = useState<string[]>([]);

    const navigate = useNavigate();

    return (
        <CreateProjectContainer>
            <GoBack onClick={() => navigate("/editions/2022/projects/")}>
                <BiArrowBack />
                Cancel
            </GoBack>
            <h2>New Project</h2>

            <NameInput name={name} setName={setName} />

            <NumberOfStudentsInput
                numberOfStudents={numberOfStudents}
                setNumberOfStudents={setNumberOfStudents}
            />

            <CoachInput
                coach={coach}
                setCoach={setCoach}
                coaches={coaches}
                setCoaches={setCoaches}
            />
            <AddedCoaches coaches={coaches} setCoaches={setCoaches} />

            <SkillInput skills={skills} setSkills={setSkills} />
            <PartnerInput partners={partners} setPartners={setPartners} />
            <CreateButton
                onClick={async () => {
                    const response = await createProject(
                        "2022",
                        name,
                        numberOfStudents!,
                        skills,
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

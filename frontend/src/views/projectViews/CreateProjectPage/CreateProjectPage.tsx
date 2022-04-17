import {
    CreateProjectContainer,
    Input,
    AddButton,
    RemoveButton,
    CreateButton,
    AddedCoach,
} from "./styles";
import { createProject } from "../../../utils/api/projects";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { GoBack } from "../ProjectDetailPage/styles";
import { BiArrowBack } from "react-icons/bi";
import { TiDeleteOutline } from "react-icons/ti";
import {
    NameInput,
    NumberOfStudentsInput,
    CoachInput,
} from "../../../components/ProjectsComponents/InputFields";

export default function CreateProjectPage() {
    const [name, setName] = useState("");
    const [numberOfStudents, setNumberOfStudents] = useState<number>(0);
    const [skills, setSkills] = useState([]);
    const [partners, setPartners] = useState([]);

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

            <div>
                {coaches.map((element, _index) => (
                    <AddedCoach key={_index}>
                        {element}
                        <RemoveButton
                            onClick={() => {
                                const newCoaches = [...coaches];
                                newCoaches.splice(_index, 1);
                                setCoaches(newCoaches);
                            }}
                        >
                            <TiDeleteOutline size={"20px"} />
                        </RemoveButton>
                    </AddedCoach>
                ))}
            </div>
            <div>
                <Input value={skills} onChange={e => setSkills([])} placeholder="Skill" />
                <AddButton>Add skill</AddButton>
            </div>
            <div>
                <Input value={partners} onChange={e => setPartners([])} placeholder="Partner" />
                <AddButton>Add partner</AddButton>
            </div>
            <CreateButton
                onClick={() =>
                    createProject("2022", name, numberOfStudents!, skills, partners, coaches)
                }
            >
                Create Project
            </CreateButton>
        </CreateProjectContainer>
    );
}

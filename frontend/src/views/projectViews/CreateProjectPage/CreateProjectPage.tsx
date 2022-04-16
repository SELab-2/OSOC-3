import { CreateProjectContainer, Input } from "./styles";
import { createProject } from "../../../utils/api/projects";
import { useState } from "react";
import { GoBack } from "../ProjectDetailPage/styles";
import { BiArrowBack } from "react-icons/bi";
import { useNavigate } from "react-router-dom";

export default function CreateProjectPage() {
    const [name, setName] = useState("");
    const [numberOfStudents, setNumberOfStudents] = useState(0);
    const [skills, setSkills] = useState([]);
    const [partners, setPartners] = useState([]);
    const [coaches, setCoaches] = useState([]);

    const navigate = useNavigate();

    return (
        <CreateProjectContainer>
            <GoBack onClick={() => navigate("/editions/2022/projects/")}>
                <BiArrowBack />
                Cancel
            </GoBack>
            <h2>New Project</h2>
            <Input
                value={name}
                onChange={e => setName(e.target.value)}
                placeholder="Project name"
            />
            <div>
                <Input
                    type="number"
                    value={numberOfStudents}
                    onChange={e => setNumberOfStudents(e.target.valueAsNumber)}
                    placeholder="Number of students"
                />
            </div>
            <div>
                <Input value={coaches} onChange={e => setCoaches([])} placeholder="Coach" />
                <button>Add</button>
            </div>
            <div>
                <Input value={skills} onChange={e => setSkills([])} placeholder="Skill" />
                <button>Add</button>
            </div>
            <div>
                <Input
                    value={partners}
                    onChange={e => setPartners([])}
                    placeholder="Partner"
                />
                <button>Add</button>
            </div>
            <button
                onClick={() =>
                    createProject("2022", name, numberOfStudents, skills, partners, coaches)
                }
            >
                Create Project
            </button>
        </CreateProjectContainer>
    );
}

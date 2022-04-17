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
            <Input
                value={name}
                onChange={e => setName(e.target.value)}
                placeholder="Project name"
            />

            <div>
                <Input
                    type="number"
                    min="0"
                    value={numberOfStudents}
                    onChange={e => setNumberOfStudents(e.target.valueAsNumber)}
                    placeholder="Number of students"
                />
            </div>
            <div>
                <Input
                    value={coach}
                    onChange={e => setCoach(e.target.value)}
                    list="users"
                    placeholder="Coach"
                />
                <datalist id="users">
                    <option value="Coach1" onClick={() => console.log("hello")} />
                    <option value="Coach2" />
                    <option value="Admin1" />
                    <option value="Admin2" />
                </datalist>
                <button
                    onClick={() => {
                        const newCoaches = [...coaches];
                        newCoaches.push(coach);
                        setCoaches(newCoaches);
                    }}
                >
                    Add coach
                </button>
            </div>
            <div>
                {coaches.map((element, _index) => (
                    <div key={_index}>
                        {element}
                        <button
                            onClick={() => {
                                const newCoaches = [...coaches];
                                newCoaches.splice(_index, 1);
                                setCoaches(newCoaches);
                            }}
                        >
                            X
                        </button>
                    </div>
                ))}
            </div>
            <div>
                <Input value={skills} onChange={e => setSkills([])} placeholder="Skill" />
                <button>Add</button>
            </div>
            <div>
                <Input value={partners} onChange={e => setPartners([])} placeholder="Partner" />
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

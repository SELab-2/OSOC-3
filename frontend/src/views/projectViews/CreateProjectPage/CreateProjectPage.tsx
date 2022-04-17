import {
    CreateProjectContainer,
    Input,
    AddButton,
    RemoveButton,
    CreateButton,
    AddedCoach,
    WarningContainer,
} from "./styles";
import { createProject } from "../../../utils/api/projects";
import { useState } from "react";
import { GoBack } from "../ProjectDetailPage/styles";
import { BiArrowBack } from "react-icons/bi";
import { useNavigate } from "react-router-dom";
import Alert from "react-bootstrap/Alert";
import { TiDeleteOutline } from "react-icons/ti";

export default function CreateProjectPage() {
    const [name, setName] = useState("");
    const [numberOfStudents, setNumberOfStudents] = useState<number>(0);
    const [skills, setSkills] = useState([]);
    const [partners, setPartners] = useState([]);

    const [coach, setCoach] = useState("");
    const [coaches, setCoaches] = useState<string[]>([]);
    const availableCoaches = ["coach1", "coach2", "admin1", "admin2"]; // TODO get users from API call

    const [showAlert, setShowAlert] = useState(false);

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
                    onChange={e => {
                        setNumberOfStudents(e.target.valueAsNumber);
                    }}
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
                    {availableCoaches.map((availableCoach, _index) => {
                        return <option key={_index} value={availableCoach} />;
                    })}
                </datalist>

                <AddButton
                    onClick={() => {
                        if (availableCoaches.some(availableCoach => availableCoach === coach)) {
                            const newCoaches = [...coaches];
                            newCoaches.push(coach);
                            setCoaches(newCoaches);
                            setShowAlert(false);
                        } else setShowAlert(true);
                    }}
                >
                    Add coach
                </AddButton>
                <WarningContainer>
                    <BadCoachAlert show={showAlert} setShow={setShowAlert}></BadCoachAlert>
                </WarningContainer>
            </div>
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

function BadCoachAlert({ show, setShow }: { show: boolean; setShow: (state: boolean) => void }) {
    if (show) {
        return (
            <Alert variant="warning" onClose={() => setShow(false)} dismissible>
                Please choose an option from the list
            </Alert>
        );
    }
    return null;
}

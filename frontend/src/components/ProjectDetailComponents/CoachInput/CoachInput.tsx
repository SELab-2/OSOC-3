import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Project } from "../../../data/interfaces";
import { User } from "../../../utils/api/users/users";

import { getCoaches } from "../../../utils/api/users/coaches";
import { Input, AddButton } from "../PartnerInput/styles";

export default function CoachInput({
    project,
    setProject,
}: {
    project: Project;
    setProject: (project: Project) => void;
}) {
    const [coach, setCoach] = useState("");
    const [availableCoaches, setAvailableCoaches] = useState<User[]>([]);

    const params = useParams();
    const editionId = params.editionId!;

    useEffect(() => {
        async function callCoaches() {
            setAvailableCoaches((await getCoaches(editionId, coach, 0))?.users || []);
        }
        callCoaches();
    }, [coach, editionId]);

    return (
        <>
            <Input
                value={coach}
                onChange={e => {
                    setCoach(e.target.value);
                }}
                list="coaches"
                placeholder="Coach"
            />

            <datalist id="coaches">
                {availableCoaches.map((availableCoach, _index) => {
                    return <option key={_index} value={availableCoach.name} />;
                })}
            </datalist>

            <AddButton
                onClick={() => {
                    addToCoaches();
                }}
            >
                Add Coach
            </AddButton>
        </>
    );

    function addToCoaches() {
        let coachToAdd = null;
        availableCoaches.forEach(availableCoach => {
            if (availableCoach.name === coach) {
                coachToAdd = availableCoach;
            }
        });
        if (coachToAdd) {
            if (!project.coaches.some(presentCoach => presentCoach.name === coach)) {
                const newCoaches = [...project.coaches];
                newCoaches.push(coachToAdd);
                setProject({ ...project, coaches: newCoaches });
            }
        }
        setCoach("");
    }
}

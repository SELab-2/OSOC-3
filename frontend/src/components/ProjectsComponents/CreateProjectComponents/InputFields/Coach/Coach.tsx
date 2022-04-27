import { useEffect, useState } from "react";
import { Alert } from "react-bootstrap";
import { useParams } from "react-router-dom";
import { getCoaches } from "../../../../../utils/api/users/coaches";
import { User } from "../../../../../utils/api/users/users";
import { AddButton, Input, WarningContainer } from "../../styles";

export default function Coach({
    coach,
    setCoach,
    coaches,
    setCoaches,
}: {
    coach: string;
    setCoach: (coach: string) => void;
    coaches: string[];
    setCoaches: (coaches: string[]) => void;
}) {
    const [showAlert, setShowAlert] = useState(false);
    const [availableCoaches, setAvailableCoaches] = useState<User[]>([]);
    const params = useParams();
    const editionId = params.editionId!;

    useEffect(() => {
        async function callCoaches() {
            setAvailableCoaches((await getCoaches(editionId, coach, 0)).users);
        }
        callCoaches();
    }, [coach, editionId]);

    return (
        <div>
            <Input
                value={coach}
                onChange={e => {
                    setCoach(e.target.value);
                }}
                list="users"
                placeholder="Coach"
            />
            <datalist id="users">
                {availableCoaches.map((availableCoach, _index) => {
                    return <option key={_index} value={availableCoach.name} />;
                })}
            </datalist>

            <AddButton
                onClick={() => {
                    if (availableCoaches.some(availableCoach => availableCoach.name === coach)) {
                        if (!coaches.includes(coach)) {
                            const newCoaches = [...coaches];
                            newCoaches.push(coach);
                            setCoaches(newCoaches);
                            setShowAlert(false);
                        }
                    } else setShowAlert(true);
                }}
            >
                Add coach
            </AddButton>
            <WarningContainer>
                <BadCoachAlert show={showAlert} setShow={setShowAlert}></BadCoachAlert>
            </WarningContainer>
        </div>
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

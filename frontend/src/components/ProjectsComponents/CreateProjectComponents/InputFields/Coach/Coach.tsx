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
    coaches: User[];
    setCoaches: (coaches: User[]) => void;
}) {
    const [showAlert, setShowAlert] = useState(false);
    const [availableCoaches, setAvailableCoaches] = useState<User[]>([]);
    const params = useParams();
    const editionId = params.editionId!;

    useEffect(() => {
        async function callCoaches() {
            setAvailableCoaches((await getCoaches(editionId, coach, 0))!.users);
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
                onKeyDown={e => {
                    if (e.key === "Enter") addCoach();
                }}
                list="users"
                placeholder="Coach"
            />
            <datalist id="users">
                {availableCoaches.map((availableCoach, _index) => {
                    return <option key={_index} value={availableCoach.name} />;
                })}
            </datalist>

            <AddButton onClick={addCoach}>Add</AddButton>
            <WarningContainer>
                <BadCoachAlert show={showAlert} setShow={setShowAlert} />
            </WarningContainer>
        </div>
    );

    function addCoach() {
        let coachToAdd = null;
        availableCoaches.forEach(availableCoach => {
            if (availableCoach.name === coach) {
                coachToAdd = availableCoach;
            }
        });
        if (coachToAdd) {
            if (!coaches.some(presentCoach => presentCoach.name === coach)) {
                const newCoaches = [...coaches];
                newCoaches.push(coachToAdd);
                setCoaches(newCoaches);
                setShowAlert(false);
            }
        } else setShowAlert(true);
        setCoach("");
    }
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

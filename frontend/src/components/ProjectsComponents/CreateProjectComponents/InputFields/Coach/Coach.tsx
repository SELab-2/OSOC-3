import { useState } from "react";
import { Alert } from "react-bootstrap";
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
    const availableCoaches = ["coach1", "coach2", "admin1", "admin2"]; // TODO get users from API call

    return (
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

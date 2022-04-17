import { TiDeleteOutline } from "react-icons/ti";
import { AddedCoach, RemoveButton } from "../styles";

export default function AddedCoaches({
    coaches,
    setCoaches,
}: {
    coaches: string[];
    setCoaches: (coaches: string[]) => void;
}) {
    return (
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
    );
}

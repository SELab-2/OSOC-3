import { TiDeleteOutline } from "react-icons/ti";
import { User } from "../../../../utils/api/users/users";
import { AddedItem, ItemName, RemoveButton } from "../styles";

export default function AddedCoaches({
    coaches,
    setCoaches,
}: {
    coaches: User[];
    setCoaches: (coaches: User[]) => void;
}) {
    return (
        <div>
            {coaches.map((element, _index) => (
                <AddedItem key={element.userId}>
                    <ItemName>{element.name}</ItemName>
                    <RemoveButton
                        onClick={() => {
                            const newItems = [...coaches];
                            newItems.splice(_index, 1);
                            setCoaches(newItems);
                        }}
                    >
                        <TiDeleteOutline size={"20px"} />
                    </RemoveButton>
                </AddedItem>
            ))}
        </div>
    );
}

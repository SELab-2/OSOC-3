import { TiDeleteOutline } from "react-icons/ti";
import { AddedItem, ItemName, RemoveButton } from "../styles";

export default function AddedItems({
    items,
    setItems,
}: {
    items: string[];
    setItems: (items: string[]) => void;
}) {
    return (
        <div>
            {items.map((element, _index) => (
                <AddedItem key={_index}>
                    <ItemName>{element}</ItemName>
                    <RemoveButton
                        onClick={() => {
                            const newItems = [...items];
                            newItems.splice(_index, 1);
                            setItems(newItems);
                        }}
                    >
                        <TiDeleteOutline size={"20px"} />
                    </RemoveButton>
                </AddedItem>
            ))}
        </div>
    );
}

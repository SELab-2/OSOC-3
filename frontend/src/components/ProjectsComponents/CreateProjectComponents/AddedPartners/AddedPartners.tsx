import { TiDeleteOutline } from "react-icons/ti";
import { DeleteButton } from "../../../Common/Buttons";
import { AddedItem, ItemName } from "../styles";

export default function AddedPartners({
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
                    <DeleteButton
                        showIcon={false}
                        onClick={() => {
                            const newItems = [...items];
                            newItems.splice(_index, 1);
                            setItems(newItems);
                        }}
                    >
                        <TiDeleteOutline size={"25px"} />
                    </DeleteButton>
                </AddedItem>
            ))}
        </div>
    );
}

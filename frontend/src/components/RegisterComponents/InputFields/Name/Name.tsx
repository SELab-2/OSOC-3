import { Input } from "../styles";

/**
 * Input field for the user's name
 * @param name getter for the state of the name
 * @param setName setter for the state of the name
 */
export default function Name({
    name,
    setName,
}: {
    name: string;
    setName: (value: string) => void;
}) {
    return (
        <div>
            <Input
                type="text"
                name="name"
                placeholder="Name"
                value={name}
                onChange={e => setName(e.target.value)}
            />
        </div>
    );
}

import { Input } from "../styles";

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

import { Input } from "../../styles";

export default function Name({ name, setName }: { name: string; setName: (name: string) => void }) {
    return (
        <Input value={name} onChange={e => setName(e.target.value)} placeholder="Project name" />
    );
}

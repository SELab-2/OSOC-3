import { Input, AddButton } from "../../styles";

export default function Partner({
    partners,
    setPartners,
}: {
    partners: string[];
    setPartners: (partners: string[]) => void;
}) {
    return (
        <div>
            <Input value={partners} onChange={e => setPartners([])} placeholder="Partner" />
            <AddButton>Add partner</AddButton>
        </div>
    );
}

import { Input } from "../../styles";

export default function InfoUrl({
    infoUrl,
    setInfoUrl,
}: {
    infoUrl: string;
    setInfoUrl: (infoUrl: string) => void;
}) {
    return (
        <Input
            value={infoUrl}
            onChange={e => setInfoUrl(e.target.value)}
            placeholder="Ex. https://osoc.be/"
        />
    );
}

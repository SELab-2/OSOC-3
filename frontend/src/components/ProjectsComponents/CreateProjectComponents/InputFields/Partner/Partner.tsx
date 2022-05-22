import { Input, AddButton } from "../../styles";

export default function Partner({
    partner,
    setPartner,
    partners,
    setPartners,
}: {
    partner: string;
    setPartner: (partner: string) => void;
    partners: string[];
    setPartners: (partners: string[]) => void;
}) {
    const availablePartners: string[] = [];

    return (
        <div>
            <Input
                value={partner}
                onChange={e => setPartner(e.target.value)}
                onKeyDown={e => {
                    if (e.key === "Enter") addPartner();
                }}
                list="partners"
                placeholder="Ex. Open Knowledge Belgium"
            />

            <datalist id="partners">
                {availablePartners.map((availablePartner, _index) => {
                    return <option key={_index} value={availablePartner} />;
                })}
            </datalist>

            <AddButton onClick={addPartner}>Add</AddButton>
        </div>
    );

    function addPartner() {
        if (!partners.includes(partner) && partner.length > 0) {
            const newPartners = [...partners];
            newPartners.push(partner);
            setPartners(newPartners);
        }
        setPartner("");
    }
}

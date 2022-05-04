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
    const availablePartners = ["partner1", "partner2"]; // TODO get partners from API call

    return (
        <div>
            <Input
                value={partner}
                onChange={e => setPartner(e.target.value)}
                list="partners"
                placeholder="Partner"
            />

            <datalist id="partners">
                {availablePartners.map((availablePartner, _index) => {
                    return <option key={_index} value={availablePartner} />;
                })}
            </datalist>

            <AddButton
                onClick={() => {
                    if (!partners.includes(partner) && partner.length > 0) {
                        const newPartners = [...partners];
                        newPartners.push(partner);
                        setPartners(newPartners);
                    }
                    setPartner("");
                }}
            >
                Add
            </AddButton>
        </div>
    );
}

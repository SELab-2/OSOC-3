import { Input } from "../styles";

export default function Email({
    email,
    setEmail,
}: {
    email: string;
    setEmail: (value: string) => void;
}) {
    return (
        <div>
            <Input
                type="email"
                name="email"
                placeholder="Email"
                value={email}
                onChange={e => setEmail(e.target.value)}
            />
        </div>
    );
}

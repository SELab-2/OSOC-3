import { Input } from "../styles";

export default function Email({ email, setEmail }: any) {
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

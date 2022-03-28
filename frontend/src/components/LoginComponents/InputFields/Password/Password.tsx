import { Input } from "../styles";

export default function Password({
    password,
    setPassword,
}: {
    password: string;
    setPassword: (value: string) => void;
}) {
    return (
        <div>
            <Input
                type="password"
                name="password"
                placeholder="Password"
                value={password}
                onChange={e => setPassword(e.target.value)}
            />
        </div>
    );
}

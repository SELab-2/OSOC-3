import { Input } from "../styles";

export default function Password({ password, setPassword }: any) {
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

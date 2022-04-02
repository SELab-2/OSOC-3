import { Input } from "../styles";

export default function Password({
    password,
    setPassword,
    callLogIn,
}: {
    password: string;
    setPassword: (value: string) => void;
    callLogIn: () => void;
}) {
    return (
        <div>
            <Input
                type="password"
                name="password"
                placeholder="Password"
                value={password}
                onChange={e => setPassword(e.target.value)}
                onKeyPress={e => {
                    if (e.key === "Enter") {
                        callLogIn();
                    }
                }}
            />
        </div>
    );
}

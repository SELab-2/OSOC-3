import { Input } from "../styles";

/**
 * Input field for passwords, authenticates when pressing the Enter key.
 * @param password getter for the state of the password
 * @param setPassword setter for the state of the password
 * @param callLogIn callback that tries to authenticate the user
 */
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

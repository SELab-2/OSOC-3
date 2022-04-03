import { Input } from "../styles";

/**
 * Input field for email addresses
 * @param email getter for the state of the email address
 * @param setEmail setter for the state of the email address
 */
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

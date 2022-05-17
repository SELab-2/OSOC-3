/**
 * React doesn't allow updating the state of the SocketProvider from inside the Navbar
 * so this is a hacky workaround that allows it :)
 */
import { useEffect } from "react";
import { useSockets } from "../../contexts/socket-context";

export default function SocketDummy({ edition }: { edition: string }) {
    const { ensureSocket } = useSockets();

    useEffect(() => {
        ensureSocket(edition);
    }, [edition, ensureSocket]);
    return null;
}

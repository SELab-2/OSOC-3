import React, { ReactNode, useContext, useState } from "react";
import { BE_DOMAIN } from "../settings";
import { getAccessToken } from "../utils/local-storage";

export interface SocketState {
    edition: string | null;
    setEdition: (value: string | null) => void;
    socket: WebSocket | null;
    setSocket: (socket: WebSocket | null) => void;
    ensureSocket: (to: string | null) => void;
}

function socketDefaultState(): SocketState {
    return {
        edition: null,
        setEdition: (_: string | null) => {},
        socket: null,
        setSocket: (_: WebSocket | null) => {},
        ensureSocket: (_: string | null) => {},
    };
}

export const SocketContext = React.createContext<SocketState>(socketDefaultState());

export function useSockets(): SocketState {
    return useContext(SocketContext);
}

function createSocketUrl(edition: string): string {
    const token = getAccessToken();
    return `ws://${BE_DOMAIN}/editions/${edition}/live?token=${token}`;
}

export function SocketProvider({ children }: { children: ReactNode }) {
    const [edition, setEdition] = useState<string | null>(null);
    const [socket, setSocket] = useState<WebSocket | null>(null);

    function ensureSocket(to: string | null) {
        // If the destination is empty, close any connections that may be open
        // This could mean that a coach was removed from their edition
        // so they should no longer be receiving events
        if (to === null) {
            if (socket !== null) {
                socket.close();
            }

            return;
        }

        // Currently connected to the required edition
        if (edition === to) {
            return;
        }

        // Already connected to another edition, close the connection first
        if (socket !== null) {
            socket.close();
        }

        // Create a websocket connection to the requested edition
        setSocket(new WebSocket(createSocketUrl(to)));
        // Save the new edition as the currently-connected edition
        setEdition(to);
    }

    const contextValue: SocketState = {
        edition: edition,
        setEdition: setEdition,
        socket: socket,
        setSocket: setSocket,
        ensureSocket: ensureSocket,
    };

    return <SocketContext.Provider value={contextValue}>{children}</SocketContext.Provider>;
}

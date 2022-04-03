import React, { useEffect, useState } from "react";
import Collapsible from "react-collapsible";
import { PendingRequestsContainer, Error } from "./styles";
import { getRequests, Request } from "../../../utils/api/users/requests";
import { RequestFilter, RequestsHeader } from "./PendingRequestsComponents";

function RequestsList(props: { loading: boolean; gotData: boolean; requests: Request[] }) {
    return null;
}

export default function PendingRequests(props: { edition: string }) {
    const [allRequests, setAllRequests] = useState<Request[]>([]);
    const [requests, setRequests] = useState<Request[]>([]);
    const [gettingRequests, setGettingRequests] = useState(false);
    const [searchTerm, setSearchTerm] = useState("");
    const [gotData, setGotData] = useState(false);
    const [open, setOpen] = useState(false);
    const [error, setError] = useState("");

    async function getData() {
        try {
            const response = await getRequests(props.edition);
            setAllRequests(response.requests);
            setRequests(response.requests);
            setGotData(true);
            setGettingRequests(false);
        } catch (exception) {
            setError("Oops, something went wrong...");
            setGettingRequests(false);
        }
    }

    useEffect(() => {
        if (!gotData && !gettingRequests && !error) {
            setGettingRequests(true);
            getData();
        }
    }, [gotData, gettingRequests, error, getData]);

    const filter = (word: string) => {
        setSearchTerm(word);
        const newRequests: Request[] = [];
        for (const request of allRequests) {
            if (request.user.name.toUpperCase().includes(word.toUpperCase())) {
                newRequests.push(request);
            }
        }
        setRequests(newRequests);
    };

    return (
        <PendingRequestsContainer>
            <Collapsible
                trigger={<RequestsHeader open={open} />}
                onOpening={() => setOpen(true)}
                onClosing={() => setOpen(false)}
            >
                <RequestFilter
                    searchTerm={searchTerm}
                    filter={word => filter(word)}
                    show={allRequests.length > 0}
                />
                <RequestsList requests={requests} loading={gettingRequests} gotData={gotData} />
                <Error> {error} </Error>
            </Collapsible>
        </PendingRequestsContainer>
    );
}

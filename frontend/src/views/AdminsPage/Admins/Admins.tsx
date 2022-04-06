import React, { useEffect, useState } from "react";
import { AdminsContainer } from "./styles";
import { getUsers, User } from "../../../utils/api/users/users";
import { getAdmins } from "../../../utils/api/users/admins";
import { Error, SearchInput } from "../../../components/UsersComponents/PendingRequests/styles";
import { AddAdmin, AdminList } from "../../../components/AdminsComponents";

export default function Admins() {
    const [allAdmins, setAllAdmins] = useState<User[]>([]);
    const [admins, setAdmins] = useState<User[]>([]);
    const [users, setUsers] = useState<User[]>([]);
    const [gettingData, setGettingData] = useState(false);
    const [searchTerm, setSearchTerm] = useState("");
    const [gotData, setGotData] = useState(false);
    const [error, setError] = useState("");

    async function getData() {
        setGettingData(true);
        setGotData(false);
        try {
            const response = await getAdmins();
            setAllAdmins(response.users);
            setAdmins(response.users);

            const usersResponse = await getUsers();
            const users = [];
            for (const user of usersResponse.users) {
                if (!response.users.some(e => e.userId === user.userId)) {
                    users.push(user);
                }
            }
            setUsers(users);

            setGotData(true);
            setGettingData(false);
        } catch (exception) {
            setError("Oops, something went wrong...");
            setGettingData(false);
        }
    }

    useEffect(() => {
        if (!gotData && !gettingData && !error) {
            getData();
        }
    }, [gotData, gettingData, error, getData]);

    const filter = (word: string) => {
        setSearchTerm(word);
        const newCoaches: User[] = [];
        for (const admin of allAdmins) {
            if (admin.name.toUpperCase().includes(word.toUpperCase())) {
                newCoaches.push(admin);
            }
        }
        setAdmins(newCoaches);
    };

    return (
        <AdminsContainer>
            <SearchInput value={searchTerm} onChange={e => filter(e.target.value)} />
            <AddAdmin users={users} refresh={getData} />
            <AdminList admins={admins} loading={gettingData} gotData={gotData} refresh={getData} />
            <Error> {error} </Error>
        </AdminsContainer>
    );
}

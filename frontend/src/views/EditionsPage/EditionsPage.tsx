/**
 * Page where users can see all editions they can access,
 * and admins can delete editions.
 */
import { useEffect, useState } from "react";
import { Edition } from "../../data/interfaces";

export default function EditionsPage() {
    const [loading, setLoading] = useState(true);
    const [editions, setEditions] = useState<Edition[]>([]);

    return (
        <div>
            <h1>Editions!</h1>
        </div>
    );
}

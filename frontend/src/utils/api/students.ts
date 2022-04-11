interface Student {
    name: string;
    amountOfSuggestions: number;
}

export async function getStudents(): Promise<Student[]> {
    return [
        { name: "King Kong", amountOfSuggestions: 4 },
        { name: "Riley Pacocha", amountOfSuggestions: 6 },
        { name: "John Barks", amountOfSuggestions: 9 },
        { name: "Tessa Hendrickx", amountOfSuggestions: 999 },
        { name: "Some Indian guy with a really long name", amountOfSuggestions: 18 },
        {
            name: "Some Indian guy with an even longer name than a really long name, damn man this name is so long it reminds me of something ;)",
            amountOfSuggestions: 123,
        },
        { name: "John Deere", amountOfSuggestions: 13 },
        { name: "Kentucky FC", amountOfSuggestions: 123456 },
        { name: "Quick Fast", amountOfSuggestions: 123456789 },
        { name: "Burger King", amountOfSuggestions: 0 },
        { name: "Take Away", amountOfSuggestions: 2 },
        { name: "Domino's Pieza", amountOfSuggestions: 4 },
        { name: "Pizza Hutte", amountOfSuggestions: 5 },
    ];
}

export interface Question {
    question: string;
    answers: string[];
    files: StudentFile[];
}

export interface StudentFile {
    filename: string;
    mimeType: string;
    url: string;
}

export interface Questions{
    suggestions: Question[];
}
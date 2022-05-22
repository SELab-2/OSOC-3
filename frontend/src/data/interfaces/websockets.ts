/**
 * Enum for the types of events sent over a websocket
 */
export enum EventType {
    PROJECT,
    PROJECT_ROLE,
    PROJECT_ROLE_SUGGESTION,
    STUDENT,
    STUDENT_SUGGESTION,
}

/**
 * Enum for the request method used when triggering this websocket event
 */
export enum RequestMethod {
    DELETE = "DELETE",
    GET = "GET",
    PATCH = "PATCH",
    POST = "POST",
}

/**
 * Basic interface for an event sent over a websocket
 */
export interface WebSocketEvent {
    method: RequestMethod;
    pathIds: {
        projectId?: string;
        studentId?: string;
        suggestionId?: string;
    };
    eventType: EventType;
}

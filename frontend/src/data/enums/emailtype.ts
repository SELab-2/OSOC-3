/**
 * Enum for the different types of emails that can be sent
 */
export enum EmailType {
    // Nothing happened (undecided/screening)
    APPLIED = "Applied",
    // We're looking for a project (maybe)
    AWAITING_PROJECT = "Awaiting Project",
    // Can participate (yes)
    APPROVED = "Approved",
    // Student signed the contract
    CONTRACT_CONFIRMED = "Contract Confirmed",
    // Student indicated they don't want to participate anymore
    CONTRACT_DECLINED = "Contract Declined",
    // We've rejected the student ourselves (no)
    REJECTED = "Rejected",
}

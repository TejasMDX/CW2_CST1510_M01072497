class ITTicket:
    """Represents an IT support ticket."""

    def __init__(self, ticket_id: int, title: str, priority: str, status: str, assigned_to: str):
        self.__id = ticket_id
        self.__title = title
        self.__priority = priority
        self.__status = status
        self.__assigned_to = assigned_to

    def assign_to(self, staff: str) -> None:
        """Assign the ticket to a staff member."""
        self.__assigned_to = staff

    def close_ticket(self) -> None:
        """Mark the ticket as closed."""
        self.__status = "Closed"

    def get_status(self) -> str:
        return self.__status

    def __str__(self) -> str:
        return (
            f"Ticket {self.__id}: {self.__title} "
            f"[{self.__priority}] – {self.__status} (assigned to: {self.__assigned_to})"
        )

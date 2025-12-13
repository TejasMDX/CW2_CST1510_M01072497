class SecurityIncident:
    """Represents a cybersecurity incident in the platform."""

    def __init__(self,category, severity, status, description, timestamp=None,incident_id = None ,reported_by=None):
        self.__id = incident_id
        self.__category = category
        self.__severity = severity
        self.__status = status
        self.__description = description
        self.__timestamp = timestamp
        self.__reported_by = reported_by

    def get_id(self):
        return self.__id
    def get_category(self):
        return self.__category
    def get_severity(self):
        return self.__severity
    def get_status(self):
        return self.__status
    def get_description(self):
        return self.__description
    def get_timestamp(self):
        return self.__timestamp
    def get_reported_by(self):
        return self.__reported_by

    def update_status(self, new_status):
        self.__status = new_status

    def get_severity_level(self):
        mapping = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        return mapping.get(self.__severity.lower(), 0)

    def __str__(self):
        return f"Incident {self.__id} [{self.__severity.upper()}] {self.__category} - {self.__status}"

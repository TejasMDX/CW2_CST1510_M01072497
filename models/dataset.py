class Dataset:
    """Represents a data science dataset in the platform."""

    def __init__(self, dataset_id: int, name: str, rows: int, columns: int, uploaded_by: str, upload_date: str):
        self.dataset_id = dataset_id
        self.name = name
        self.rows = rows
        self.columns = columns
        self.uploaded_by = uploaded_by
        self.upload_date = upload_date

    def __str__(self) -> str:
        return (
            f"Dataset {self.dataset_id}: {self.name} "
            f"({self.rows} rows, {self.columns} columns, uploaded by {self.uploaded_by} on {self.upload_date})"
        )

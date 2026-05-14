from datetime import datetime, timedelta


class ProjectReportData:
    """Данные о проекте для отчёта."""

    def __init__(
        self,
        name: str,
        description: str,
        create_date: datetime,
        close_date: datetime,
    ):
        self.name = name
        self.description = description
        self.create_date = create_date
        self.close_date = close_date
        self.collection_time: timedelta = close_date - create_date

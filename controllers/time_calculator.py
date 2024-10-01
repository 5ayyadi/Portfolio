from datetime import datetime
from models import Person

def calculate_age(person: Person) -> int:
        # Convert string to datetime and calculate age
        birthday = datetime.strptime(person.birthday, '%Y-%m-%d')
        today = datetime.today()
        return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

def calculate_duration(start: str, end: str | None = None) -> tuple[int,int]:
        """
			calculate the period between two given dates

        Args:
            start (str): starting date
            end (str): ending date

        Returns:
            tuple (year, month): duration in years and months
        """
        start_date = datetime.strptime(start, "%Y-%m")
        if end is None:
            end_date = datetime.today()
        else:
            end_date = datetime.strptime(end, "%Y-%m")
        year = end_date.year - start_date.year
        
        month = end_date.month - start_date.month
        
        if month < 0:
            year -= 1
            month += 12
        
        return year, month
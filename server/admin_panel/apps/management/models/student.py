from ...management.models import CustomUser


class Student(CustomUser):

    def __str__(self):
        return f"{self.id} - {self.phone_number}"

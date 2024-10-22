import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmployeesProject.settings')
django.setup()

from app.models import Position, User

def create_records():
    positions = [
       Position(title='INACTIVE EMPLOYEE', rights_level=1),
       Position(title='EMPLOYEE', rights_level=2),
       Position(title='MANAGER', rights_level=3),
       Position(title='ADMIN', rights_level=4),
    ]
    Position.objects.bulk_create(positions)

    inactive_employee = Position.objects.get(title='INACTIVE EMPLOYEE')
    employee = Position.objects.get(title='EMPLOYEE')
    manager = Position.objects.get(title='MANAGER')
    admin = Position.objects.get(title='ADMIN')


    users_data = [
        ('John', 'Doe', 'password', inactive_employee, '2025-01-01'),
        ('Alice', 'Smith', 'password', employee, '2025-01-02'),
        ('Brian', 'White', 'password', manager, '2025-01-03'),
        ('Catherine', 'Johnson', 'password', admin, '2025-01-04'),
        ('Michael', 'Orange', 'password', inactive_employee, '2025-01-05'),
        ('Laura', 'Clark', 'password', employee, '2025-01-06'),
    ]

    users = []
    for first_name, last_name, password, position, date_joined in users_data:
        user = User(username=first_name, first_name=first_name, last_name=last_name, position=position,
                    date_joined=date_joined)
        user.set_password(password)
        users.append(user)

    User.objects.bulk_create(users)
    print("Records created successfully.")

if __name__ == "__main__":
    create_records()
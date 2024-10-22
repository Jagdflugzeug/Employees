# EmployeesProject

### Установите зависимости в виртуальном окружении и инициализируйте локальную базу данных SQLite3
### выполните скрипт настройки окружения разработки: ./dev_setup.sh
### либо вручную

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py makemigrations app
python3 manage.py migrate
```

### опционально можно создать суперпользователя
```bash
python3 manage.py createsuperuser
python3 manage.py createsuperuser
```

### наполнение базы данных
Последним шагом скрипт dev_setup.sh выполняет setup_db.py, который наполняет базу данных. 
Это позволит вам залогиниться одним из созданных скриптом пользователей. Например, пользователь:
```bash
Имя: Catherine
Пароль: password
Позволит получить права уровня ADMIN.
```
---

## запуск 
```bash
python3 manage.py runserver
```
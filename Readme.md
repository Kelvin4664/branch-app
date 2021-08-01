### Setup instructions:
1. Create a python virtual environment: https://realpython.com/lessons/creating-virtual-environment/
2. Install dependencies: `pip install -r requirements.txt`
3. Apply migrations: `python manage.py migrate`
4. Create a superuser: `python manage.py createsuperuser`and follow the prompt
5. Start the development server: `python manage.py runserver`
6. Navigate to the admin site at http://127.0.0.1:8000 and login with the superuser credentials you created
7. Navigate to the users tab and add new users and set type to either user or agent
8. Navigate to http://127.0.0.1:8000 on multiple tabs and sign in as clients and agents
9. In any of the clients tab, enter a message and it should show up instantly in any of the agent's tab.
import requests

statement_generation_service = 'http://127.0.0.1:8001'

def generate_monthly_statement(user_id: int, month: int, year: int) -> None:
    '''
    Calls generate monthly statement api
    '''
    url = f'{statement_generation_service}/statement/{user_id}/{month}/{year}'

    try:
        response = requests.post(url)

        print('yoyoy')
        print(response)

        if response.status_code == 201:
            return True
    except Exception as e:
        print(f"Error while generating monthly statement for {user_id}: {str(e)}")
        return False

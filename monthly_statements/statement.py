import requests

statement_generation_service = 'http://statement-generation-service:8001'

def generate_monthly_statement(user_id: int, month: int, year: int) -> None:
    '''
    Calls generate monthly statement api
    '''
    url = f'{statement_generation_service}/statement/{user_id}/{month}/{year}'

    try:
        response = requests.post(url)
        response.raise_for_status()

        print(response.text)
        if response.status_code == 201:
            body = response.json()
            print(body)
            return True
    except Exception as e:
        print(f"Error while generating monthly statement for {user_id}: {str(e)}")
        return False

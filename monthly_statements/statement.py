import requests

statement_generation_service = 'http://statement-generation-service:8081'

def generate_monthly_statement(user_id: int, month: int, year: int) -> None:
    '''
    Calls generate monthly statement api
    '''
    url = f'{statement_generation_service}/{user_id}/{month}/{year}'

    try:
        response = requests.post(url)

        if response.status_code == 201:
            return True
    except Exception as e:
        print(f"Error while generating monthly statement for {user_id}: {str(e)}")
        return False

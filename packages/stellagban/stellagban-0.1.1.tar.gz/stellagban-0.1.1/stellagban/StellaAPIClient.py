import requests
import html

class Client:
    
    def __init__(self, api_key: str, host: str = 'https://stellagban.herokuapp.com//api/v1') -> None:
        self.host = host
        self.api_key = api_key 
        
    def gban_protocol(self, admin_id, GbannedUser, reason):
        URL = f'{self.host}/admin/gban/'

        headers = {
            'API_KEY': self.api_key
        }
            
        GbanData = {
            'admin': admin_id,
            'gbanned_user': GbannedUser,
            'reason': reason
        } 
        
        ReturnedData = requests.post(
            url=URL,
            json=GbanData,
            headers=headers
            )

        if ReturnedData.status_code == requests.codes.ok:
            requestedData = ReturnedData.json()
            
            operation = requestedData['operation']
            status = requestedData['status']

            return (
                operation,
                status
            )
    
    def ungban_protocol(self, user_id):
        URL = f'{self.host}/admin/ungban/'

        headers = {
            'API_KEY': self.api_key
        }

        USER_DATA = {
        'user_id': user_id
        }

        ReturnedData = requests.delete(
            url=URL,
            json=USER_DATA,
            headers=headers
            )
        
        ReturnedJson = ReturnedData.json()
        if ReturnedData.status_code == requests.codes.ok:
            status = ReturnedJson['status']
            operation = ReturnedJson['operation']

            return (
                status, 
                operation
            )
        else:
            return (
                'Server is currently down!',
                False
            )
    
    def banned_list(self) -> list:
        URL = f'{self.host}/admin/users/'

        headers = {
            'API_KEY': self.api_key
        }

        ReturnedData = requests.get(
            url=URL,
            headers=headers
        )

        return ReturnedData
    
    def apis_list(self) -> list:
        URL = f'{self.host}/admin/apis/'

        headers = {
            'API_KEY': self.api_key
        }

        ReturnedData = requests.get(
            url=URL,
            headers=headers
        )

        return ReturnedData

    def generate_api(self, user_id, first_name, username):
        URL = f'{self.host}/generate/'

        headers = {
            'API_KEY': self.api_key
        }

        USER_DATA = {
        'user_id': user_id,
        'first_name': html.escape(first_name),
        'username': username
        }

        ReturnedData = requests.post(
            url=URL,
            json=USER_DATA,
            headers=headers
            )
        
        ReturnedJson = ReturnedData.json()
        if ReturnedData.status_code == requests.codes.ok:
            api_key = ReturnedJson['api_key']
            operation = ReturnedJson['operation']

            return (
                operation,
                api_key
            )
        else:
            return (
                'Server is currently down!',
                False
            )
    
    def promote_api(self, user_id):
        URL = f'{self.host}/admin/promote/'

        headers = {
            'API_KEY': self.api_key
        }

        USER_DATA = {
        'user_id': user_id
        }

        ReturnedData = requests.post(
            url=URL,
            json=USER_DATA,
            headers=headers
            )

        ReturnedJson = ReturnedData.json()
        if ReturnedData.status_code == requests.codes.ok:
            status = ReturnedJson['status']
            operation = ReturnedJson['operation']

            return (
                status, 
                operation
            )
        else:
            return (
                'Server is currently down!',
                False
            )
    
    


        




        
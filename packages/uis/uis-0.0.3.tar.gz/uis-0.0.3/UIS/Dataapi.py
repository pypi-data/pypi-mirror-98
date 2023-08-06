#
# v1.0
#   - init
#   - login
#   - logout
#   - get_call_leg_report
#
# v1.1
#   - get_account
#   - get_sip_lines
#
# v1.2
#   - last_exception
#   - upload_offline_messages
#   - set_tag_sales
#   - delete_offline_messages
import requests
import json


class Dataapi:
    _url = "https://dataapi.uiscom.ru/v2.0"
    is_auth = False
    session = None
    app_id = None
    expire_at = None
    last_request = None
    last_exception = None

    def __init__(self, token=None, user=None, password=None):
        self.access_token = token
        self.user = user
        self.password = password
        self.session = requests.Session()
        if (user is not None and password is not None):
            self.login()

    async def login(self, user=None, password=None, token=None):
        if (user is not None and password is not None):
            self.access_token = token
            self.user = user
        elif (self.user is None and self.password is None):
            self.is_auth = False
            return False
        else:
            json_request = {
                "jsonrpc": "2.0",
                "id": "req1",
                "method": "login.user",
                "params": {
                    "login": self.user,
                    "password": self.password
                }
            }
            response = self.session.post(self._url, json=json_request)
            if response.status_code == 200:
                response_json = json.loads(response.content)
                tkn = response_json['result']['data']['access_token']
                self.access_token = tkn
                self.app_id = response_json['result']['data']['app_id']
                self.expire_at = response_json['result']['data']['expire_at']
                self.is_auth = True
                return True
            else:
                return False
            pass

    async def logout(self):
        if self.is_auth is not None:
            json_request = {
                "jsonrpc": "2.0",
                "id": "req1",
                "method": "logout.user",
                "params": {
                    "access_token": self.access_token
                }
            }
            response = self.session.post(self._url, json=json_request)
            if response.status_code == 200:
                self.token = self.app_id = self.expire_at = None
                self.is_auth = False
                return True

    async def get_call_leg_report(self, session_id, start_time, finish_time):
        try:
            json_request = {
                "id": 1,
                "jsonrpc": "2.0",
                "method": "get.call_legs_report",
                "params":
                    {
                        "filter": {
                            "field": "call_session_id",
                            "operator": "=",
                            "value": session_id
                        },
                        "fields": [
                            "id",
                            "called_phone_number",
                            "calling_phone_number",
                            "virtual_phone_number",
                            "employee_id",
                            "employee_full_name",
                            "is_operator",
                            "call_records",
                            "duration",
                            "total_duration",
                            "direction",
                            "is_transfered",
                            "is_talked"
                        ],
                        "access_token": self.access_token,
                        "date_from": start_time,
                        "date_till": finish_time
                    }
            }
            self.last_request = json_request
            response = self.session.post(self._url, json=json_request)
            if response.status_code == 200:
                return json.loads(response.content)
        except Exception as e:
            self.last_exception = e
            return None

    async def get_account(self):
        try:
            json_request = {
                "id": 1,
                "jsonrpc": "2.0",
                "method": "get.account",
                "params":
                    {
                        "access_token": self.access_token,
                    }
            }
            self.last_request = json_request
            response = self.session.post(self._url, json=json_request)
            if response.status_code == 200:
                return json.loads(response.content)
        except Exception as e:
            self.last_exception = e
            return None

    async def get_employees_ext(self, ext, log=None):
        try:
            json_request = {
                "id": 1,
                "jsonrpc": "2.0",
                "method": "get.employees",
                "params":
                    {
                        "access_token": self.access_token,
                        "filter": {
                            "field": "extension",
                            "operator": "jsquery",
                            "value": "extension_phone_number=\"" + ext + "\""
                        },
                        "fields": [
                            "id"
                        ]
                    }
            }
            self.last_request = json_request
            response = self.session.post(self._url, json=json_request)
            if log is not None:
                await log(
                    dataapi_response=response.content,
                    dataapi_request=json_request)
            if response.status_code == 200:
                return json.loads(response.content)
        except Exception as e:
            self.last_exception = e
            return None

    async def get_employees_id(self, id_user, log=None):
        try:
            json_request = {
                "id": 1,
                "jsonrpc": "2.0",
                "method": "get.employees",
                "params":
                    {
                        "access_token": self.access_token,
                        "filter": {
                            "field": "id",
                            "operator": "=",
                            "value": id_user
                        },
                        "fields": [
                            "extension"
                        ]
                    }
            }
            response = self.session.post(self._url, json=json_request)
            if log is not None:
                await log(
                    dataapi_response=response.content,
                    dataapi_request=json_request)
            if response.status_code == 200:
                return json.loads(response.content)
        except Exception as e:
            self.last_exception = e
            return None

    async def get_sip_lines_employee_id(self, employee_id, log=None):
        try:
            json_request = {
                "jsonrpc": "2.0",
                "id": "number",
                "method": "get.sip_lines",
                "params": {
                    "access_token": self.access_token,
                    "filter": {
                        "field": "employee_id",
                        "operator": "=",
                        "value": employee_id
                    },
                    "fields": [
                        "physical_state",
                        "virtual_phone_number",
                        "type",
                        "virtual_phone_number"
                    ]
                }
            }
            self.last_request = json_request
            response = self.session.post(self._url, json=json_request)
            if log is not None:
                await log(
                    dataapi_response=response.content,
                    dataapi_request=json_request)
            if response.status_code == 200:
                return json.loads(response.content)
        except Exception as e:
            self.last_exception = e
            return None

    async def upload_offline_messages(  # only one message
            self,
            log=None,
            date_time=None,
            name=None,
            phone=None,
            email=None,
            message=None,
            visitor_session_id=None,
            campaign_id=None,
            site_id=None
    ):
        try:
            json_request = {
                "jsonrpc": "2.0",
                "id": "number",
                "method": "upload.offline_messages",
                "params": {
                    "access_token": self.access_token,
                    "offline_messages": []
                }
            }
            params_messages = {}  # json_request['params']['offline_messages']
            if date_time is not None:
                params_messages['date_time'] = date_time
            if name is not None:
                params_messages['name'] = name
            if phone is not None:
                params_messages['phone'] = phone
            if email is not None:
                params_messages['email'] = email
            if message is not None:
                params_messages['message'] = message
            if visitor_session_id is not None:
                params_messages['visitor_session_id'] = visitor_session_id
            if campaign_id is not None:
                params_messages['campaign_id'] = campaign_id
            if site_id is not None:
                params_messages['site_id'] = site_id
            json_request['params']['offline_messages'].append(params_messages)

            self.last_request = json_request
            response = self.session.post(self._url, json=json_request)
            if log is not None:
                await log(
                    dataapi_response=response.content,
                    dataapi_request=json_request)
            if response.status_code == 200:
                return json.loads(response.content)
            return None
        except Exception as e:
            self.last_exception = e
            return None

    async def set_tag_sales(

            self,
            communication_id,
            communication_type,
            date_time,
            transaction_value,
            comment=None,
            log=None
    ):
        """ Returns dict

            Parameters:
                communication_id (int)
                communication_type (enum): chat, call, goal, offline_message
                date_time (iso8601): YYYY-MM-DD hh:mm:ss (Дата и время сделки)
                transaction_value (number): Стоимость сделки
                comment (string): Максимальная длина 255 символов
                log

            Returns:
               {
                  "jsonrpc":"2.0",
                  "id":"number",
                  "result":{
                    "id":"number"
                  }
                }
        """
        try:
            json_request = {
                "jsonrpc": "2.0",
                "id": "number",
                "method": "set.tag_sales",
                "params": {
                    "access_token": self.access_token
                }
            }
            params = json_request['params']
            params['communication_id'] = communication_id
            params['communication_type'] = communication_type
            params['date_time'] = date_time
            params['transaction_value'] = transaction_value
            if comment is not None:
                params['comment'] = comment
            self.last_request = json_request
            response = self.session.post(self._url, json=json_request)
            if log is not None:
                await log(
                    dataapi_response=response.content,
                    dataapi_request=json_request)
            if response.status_code == 200:
                return json.loads(response.content)
            return None
        except Exception as e:
            self.last_exception = e
            return None

    async def delete_offline_messages(self, communication_id):
        try:
            json_request = {
                "jsonrpc": "2.0",
                "id": "number",
                "method": "delete.offline_messages",
                "params": {
                    "access_token": self.access_token,
                    "id": communication_id
                }
            }
            self.last_request = json_request
            response = self.session.post(self._url, json=json_request)
            if response.status_code == 200:
                return json.loads(response.content)
            return None
        except Exception as e:
            self.last_exception = e
            return None


# if __name__ == '__main__':
#     import asyncio
#
#     dataapi = Dataapi(token='27ttr4bczzvtymacirw631cf670x3fyupbliuil8')
#
#     res = asyncio.run(dataapi.upload_offline_messages(
#         visitor_session_id=4808337936,
#         name='Ivan5',
#         phone='79991234567',
#         message='сообщение1'
#     ))
#     id_communication = res['result']['data'][0]['id']
#     res = asyncio.run(dataapi.set_tag_sales(
#         communication_id=id_communication,
#         communication_type='offline_message',
#         date_time='2020-06-21 11:10:00',
#         transaction_value=1000,
#         comment='Комментарий при продаже'
#     ))
#     pass

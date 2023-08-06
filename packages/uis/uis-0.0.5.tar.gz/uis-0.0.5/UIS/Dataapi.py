import requests
import json


class Dataapi:
    """
    Версии

    0.0.5
        + add login
        + add logout
        + add get_call_leg_report
    """
    _url = "https://dataapi.uiscom.ru/v2.0"
    _session = None
    _expire_at = None
    _access_token = None
    _user = None
    _password = None

    is_auth = False
    app_id = None
    last_request = None
    last_exception = None

    def __init__(self,
                 token: str = None,
                 user: str = None,
                 password: str = None):
        """Класс dataapi используется для работы с API
        Ссылка на API [https://comagic.github.io/data-api/]

        Note:
            Если в инициализации установлены параметры логина и пароля,
            то происходит выполнения метода login для предварительной
            авторизации и использования в дальнейшем функциями

        :param token: API ключ (Вместо логина и пароля)
        :param user: Логин пользователя (вместо api token)
        :param password: Пароль пользователя (вместо api token)

        Methods:
        -------
            login: Авторизация по логину

            logout: Разлогиниться в api (если ранее был использован login)

            get_call_leg_report: Получение списка CDR по сессии звонка
        """
        self._access_token = token
        self._user = user
        self._password = password
        self._session = requests.Session()
        if (user is not None and password is not None):
            self.login()

    async def login(self, user=None, password=None):
        """
        :param user: логин пользователя (вместо token)
        :param password: пароль пользователя (вместо token)
        :return: bool
        """
        if (user is not None and password is not None):
            self._user = user
            self._password = password
        elif (self._user is None and self._password is None):
            self.is_auth = False
            return False
        else:
            json_request = {
                "jsonrpc": "2.0",
                "id": "req1",
                "method": "login.user",
                "params": {
                    "login": self._user,
                    "password": self._password
                }
            }
            response = self._session.post(self._url, json=json_request)
            if response.status_code == 200:
                response_json = json.loads(response.content)
                tkn = response_json['result']['data']['access_token']
                self._access_token = tkn
                self.app_id = response_json['result']['data']['app_id']
                self._expire_at = response_json['result']['data']['expire_at']
                self.is_auth = True
                return True
            else:
                self.last_exception = response.content.decode()
                return False
            pass

    async def logout(self):
        """
        :return: bool
        """
        if self.is_auth is not None:
            json_request = {
                "jsonrpc": "2.0",
                "id": "req1",
                "method": "logout.user",
                "params": {
                    "access_token": self._access_token
                }
            }
            response = self._session.post(self._url, json=json_request)
            if response.status_code == 200:
                self._access_token = self.app_id = self._expire_at = None
                self.is_auth = False
                return True
            else:
                self.last_exception = response.content.decode()
                return False

    async def get_call_leg_report(
            self,
            session_id: int,
            start_time: str,
            finish_time: str
    ):
        """
        Получение списка CDR по сессии звонка.

        :param session_id: Уникальный идентификатор сессии звонка
        :param start_time: 	Дата начала выборки (date_from).
            iso8601	YYYY-MM-DD hh:mm:ss
        :param finish_time: Дата окончания выбокри (date_till)
            iso8601	YYYY-MM-DD hh:mm:ss
        :return: None: Запрос с ошибкой. json: ответ сервера

        Поля в ответе:
        ----
        * id: Уникальный идентификатор CDR
        * called_phone_number: Номер кому звонили
        * calling_phone_number: Номер звонящего
        * virtual_phone_number: Виртуальный номер
        * employee_id: 	Уникальный идентификатор сотрудника, кому звонили
        * employee_full_name: Ф.И.О. сотрудника, кому звонили
        * is_operator:	Принадлежит ли это плечо оператору
        * call_records: Уникальный идентификатор ссылки на записанный разговор.
            Можно прослушать вызвав запрос в браузере:
            http://app.comagic.ru/system/media/talk/{call_session_id}/
            {уникальный идентификатор ссылки на записанный разговор}
        * duration: 	Продолжительность плеча с начала поднятия трубки.
            Значение в секундах
        * total_duration: Общая продолжительность плеча. Значение в секундах
        * direction: Направление плеча
        * is_transfered: Трансферное ли это плечо
        * is_talked: Состоялся ли разговор
        """
        json_request = None
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
                        "access_token": self._access_token,
                        "date_from": start_time,
                        "date_till": finish_time
                    }
            }
            self.last_request = json_request
            response = self._session.post(self._url, json=json_request)
            if response.status_code == 200:
                return json.loads(response.content)
        except Exception as e:
            self.last_request = json_request
            self.last_exception = e
            return None

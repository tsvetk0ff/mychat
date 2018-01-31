import time as ctime
from .config import *
from .exceptions import WrongParamsError, ToLongError, WrongActionError, WrongDictError, ResponseCodeError


class MaxLengthField:
    """Дескриптор ограничивающий размер поля"""

    def __init__(self, name, max_length):
        """
        :param name: имя поля
        :param max_length: максимальная длина
        """
        self.max_length = max_length
        self.name = '_' + name

    def __set__(self, instance, value):
        # если длина поля больше максимального значения
        if len(value) > self.max_length:
            # вызываем ошибку
            raise ToLongError(self.name, value, self.max_length)
        # иначе записываем данные в поле
        setattr(instance, self.name, value)

    def __get__(self, instance, owner):
        # получаем данные поля
        return getattr(instance, self.name)


class Jim:
    def to_dict(self):
        return {}

    @staticmethod
    def try_create(jim_class, input_dict):
        try:
            return jim_class(**input_dict)
        except KeyError:
            raise WrongParamsError(input_dict)

    @staticmethod
    def from_dict(input_dict):
        """Наиболее важный метод создания объекта из входного словаря
        :input_dict: входной словарь
        :return: объект Jim: Action или Response
        """
        # должно быть response или action
        # если action
        if ACTION in input_dict:
            # достаем действие
            action = input_dict.pop(ACTION)
            # действие должно быть в списке действий
            if action in ACTIONS:
                if action == PRESENCE:
                    return Jim.try_create(JimPresence, input_dict)
                elif action == GET_CONTACTS:
                    return Jim.try_create(JimGetContacts, input_dict)
                elif action == CONTACT_LIST:
                    return Jim.try_create(JimContactList, input_dict)
                elif action == ADD_CONTACT:
                    return Jim.try_create(JimAddContact, input_dict)
                elif action == DEL_CONTACT:
                    return Jim.try_create(JimDelContact, input_dict)
                elif action == MSG:
                    try:
                        input_dict['from_'] = input_dict['from']
                    except KeyError:
                        raise WrongParamsError(input_dict)
                    del input_dict['from']
                    return Jim.try_create(JimMessage, input_dict)
            else:
                raise WrongActionError(action)
        elif RESPONSE in input_dict:
            return Jim.try_create(JimResponse, input_dict)
        else:
            raise WrongDictError(input_dict)


class JimAction(Jim):
    # __slots__ = (ACTION, TIME) - со слотами не работает __dict__ - а он нам нужен для перевода в json

    def __init__(self, action, time=None):
        self.action = action
        if time:
            self.time = time
        else:
            self.time = ctime.time()

    def to_dict(self):
        result = super().to_dict()
        result[ACTION] = self.action
        result[TIME] = self.time
        return result


class JimPresence(JimAction):
    # Имя пользователя ограничено 25 символами - используем дескриптор
    account_name = MaxLengthField('account_name', USERNAME_MAX_LENGTH)

    # __slots__ = (ACTION, ACCOUNT_NAME, TIME) - дескриптор конфилктует со слотами

    def __init__(self, account_name, time=None):
        self.account_name = account_name
        super().__init__(PRESENCE, time)

    def to_dict(self):
        result = super().to_dict()
        result[ACCOUNT_NAME] = self.account_name
        return result


class JimGetContacts(JimAction):
    # Имя пользователя ограничено 25 символов - используем дескриптор
    account_name = MaxLengthField('account_name', USERNAME_MAX_LENGTH)

    def __init__(self, account_name, time=None):
        self.account_name = account_name
        super().__init__(GET_CONTACTS, time)

    def to_dict(self):
        result = super().to_dict()
        result[ACCOUNT_NAME] = self.account_name
        return result


class JimContactList(JimAction):
    user_id = MaxLengthField('user_id', USERNAME_MAX_LENGTH)

    def __init__(self, user_id, time=None):
        self.user_id = user_id
        super().__init__(CONTACT_LIST, time)

    def to_dict(self):
        result = super().to_dict()
        result[USER_ID] = self.user_id
        return result


class JimAddContact(JimAction):
    account_name = MaxLengthField('account_name', USERNAME_MAX_LENGTH)
    user_id = MaxLengthField('user_id', USERNAME_MAX_LENGTH)

    def __init__(self, account_name, user_id, time=None):
        self.account_name = account_name
        self.user_id = user_id
        super().__init__(ADD_CONTACT, time)

    def to_dict(self):
        result = super().to_dict()
        result[ACCOUNT_NAME] = self.account_name
        result[USER_ID] = self.user_id
        return result


class JimDelContact(JimAction):
    account_name = MaxLengthField('account_name', USERNAME_MAX_LENGTH)
    user_id = MaxLengthField('user_id', USERNAME_MAX_LENGTH)

    def __init__(self, account_name, user_id, time=None):
        self.account_name = account_name
        self.user_id = user_id
        super().__init__(DEL_CONTACT, time)

    def to_dict(self):
        result = super().to_dict()
        result[ACCOUNT_NAME] = self.account_name
        result[USER_ID] = self.user_id
        return result


class JimMessage(JimAction):
    to = MaxLengthField('to', USERNAME_MAX_LENGTH)
    from_ = MaxLengthField('from', USERNAME_MAX_LENGTH)
    message = MaxLengthField('message', MESSAGE_MAX_LENGTH)

    def __init__(self, to, from_, message, time=None):
        self.to = to
        self.from_ = from_
        self.message = message
        super().__init__(MSG, time=time)

    def to_dict(self):
        result = super().to_dict()
        result[TO] = self.to
        result[FROM] = self.from_
        result[MESSAGE] = self.message
        return result


class ResponseField:
    def __init__(self, name):
        """
        :param name: имя поля
        """
        self.name = '_' + name

    def __set__(self, instance, value):
        if value not in RESPONSE_CODES:
            raise ResponseCodeError
        setattr(instance, self.name, value)

    def __get__(self, instance, owner):
        return getattr(instance, self.name)


class JimResponse(Jim):
    response = ResponseField('response')

    def __init__(self, response, error=None, alert=None, quantity=None):
        self.response = response
        self.error = error
        self.alert = alert
        self.quantity = quantity

    def to_dict(self):
        result = super().to_dict()
        result[RESPONSE] = self.response
        if self.error is not None:
            result[ERROR] = self.error
        if self.alert is not None:
            result[ALERT] = self.alert
        if self.quantity is not None:
            result[QUANTITY] = self.quantity
        return result

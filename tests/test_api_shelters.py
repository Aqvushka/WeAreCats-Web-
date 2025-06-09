from requests import get, put, post, delete


def test_get():
    print('Успешное получение списка всех приютов')
    print(get('http://127.0.0.1:8080/api/shelters').json())
    print('Успешное получение одного приюта')
    print(get('http://127.0.0.1:8080/api/shelters/1').json())
    print('Ошибка запоса - неверный id')
    print(get('http://127.0.0.1:8080/api/shelters/1000').json())
    print('Ошибка запроса - строка')
    print(get('http://127.0.0.1:8080/api/shelters/b').json())


def test_add():
    print('Ошибка запроса - пустой JSON')
    print(post('http://127.0.0.1:8080/api/shelters', json={}).json())
    print('Ошибка запроса - указание id')
    print(post('http://127.0.0.1:8080/api/shelters', json={'id': 4}).json())
    print('Ошибка запорса - не полный JSON')
    print(post('http://127.0.0.1:8080/api/shelters', json={'name': 'Приют'}).json())
    print('Успешное добавление')
    print(post('http://127.0.0.1:8080/api/shelters', json={'name': 'Тестовый Приют',
                                                           'address': 'Улица1',
                                                           'phone': '000-000',
                                                           'user_id': 1,
                                                           'validated': 1}).json())


def test_delete():
    print('Ошибка запроса - неверный id')
    print(delete('http://127.0.0.1:8080/api/shelters/1000').json())
    print('Ошибка запроса - строка')
    print(delete('http://127.0.0.1:8080/api/shelters/b').json())
    print('Список приютов до удаления')
    print(get('http://127.0.0.1:8080/api/shelters').json())
    print('Успешное удаление')
    print(delete('http://127.0.0.1:8080/api/shelters/2').json())
    print('Список приютов после удаления')
    print(get('http://127.0.0.1:8080/api/shelters').json())


def test_refactor():
    print('Ошибка запроса - попытка изменения id')
    print(put('http://127.0.0.1:8080/api/shelters/1', json={'id': 4}).json())
    print('Ошибка запроса - несуществующий пользователь')
    print(put('http://127.0.0.1:8080/api/shelters/2', json={'user_id': 1000}).json())
    print('Список приютов до изменения')
    print(get('http://127.0.0.1:8080/api/shelters').json())
    print('Успешное изменение')
    print(put('http://127.0.0.1:8080/api/shelters/2', json={'name': 'Теперь не тестовый',
                                                            'user_id': 1}).json())
    print('Список приютов после изменения')
    print(get('http://127.0.0.1:8080/api/shelters').json())


def test_is_shelter():
    print(get('http://127.0.0.1:8080/api/shelters').json())
    print(post('http://127.0.0.1:8080/api/shelters', json={'name': 'Приют для 2((((',
                                                           'address': '1',
                                                           'phone': '005-130',
                                                           'user_id': 2,
                                                           'validated': 1}).json())
    print(put('http://127.0.0.1:8080/api/shelters/4', json={'name': 'Приют для 2',
                                                            'user_id': 3}).json())


if __name__ == '__main__':
    test_get()
    """test_add()"""
    """test_refactor()"""
    """test_delete()"""
    test_is_shelter()
    test_get()

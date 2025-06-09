from requests import get, put, post, delete


def test_get():
    print(get('http://127.0.0.1:8080/api/users').json())
    print(get('http://127.0.0.1:8080/api/users/1').json())
    print(get('http://127.0.0.1:8080/api/users/1000').json())
    print(get('http://127.0.0.1:8080/api/users/b').json())


def test_add():
    print(post('http://127.0.0.1:8080/api/users', json={}).json())
    print(post('http://127.0.0.1:8080/api/users', json={'id': 4}).json())
    print(post('http://127.0.0.1:8080/api/users', json={'login': 'user'}).json())
    print(post('http://127.0.0.1:8080/api/users', json={'login': 'user',
                                                        'email': 'un@mail.ru',
                                                        'password': '123'}).json())


def test_delete():
    print(delete('http://127.0.0.1:8080/api/users/1000').json())
    print(delete('http://127.0.0.1:8080/api/users/b').json())
    print(get('http://127.0.0.1:8080/api/users').json())
    print(delete('http://127.0.0.1:8080/api/users/2').json())
    print(get('http://127.0.0.1:8080/api/users').json())


def test_refactor():
    print('Ошибка запроса - попытка изменения id')
    print(put('http://127.0.0.1:8080/api/users/1', json={'id': 4}).json())
    print(put('http://127.0.0.1:8080/api/users/1000', json={}).json())
    print(get('http://127.0.0.1:8080/api/users').json())
    print('Успешное изменение')
    print(put('http://127.0.0.1:8080/api/users/3', json={'login': 'userNEW',
                                                         'email': 'unNEW@mail.ru'}).json())
    print(get('http://127.0.0.1:8080/api/users').json())


if __name__ == '__main__':
    """test_get()
    test_add()"""
    test_refactor()
    """test_delete()"""

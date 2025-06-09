from requests import get, put, post, delete


def test_get():
    print('Успешное получение списка всех котов')
    print(get('http://127.0.0.1:8080/api/cats').json())
    print('Успешное получение одного кота')
    print(get('http://127.0.0.1:8080/api/cats/1').json())
    print('Ошибка запоса - неверный id')
    print(get('http://127.0.0.1:8080/api/cats/1000').json())
    print('Ошибка запроса - строка')
    print(get('http://127.0.0.1:8080/api/cats/b').json())


def test_add():
    print('Ошибка запроса - пустой JSON')
    print(post('http://127.0.0.1:8080/api/cats', json={}).json())
    print('Ошибка запроса - указание id')
    print(post('http://127.0.0.1:8080/api/cats', json={'id': 4}).json())
    print('Ошибка запорса - не полный JSON')
    print(post('http://127.0.0.1:8080/api/cats', json={'name': 'Барсик'}).json())
    print('Успешное добавление')
    print(post('http://127.0.0.1:8080/api/cats', json={'name': 'Барсик',
                                                       'shelter_id': 1}).json())


def test_delete():
    print('Ошибка запроса - неверный id')
    print(delete('http://127.0.0.1:8080/api/cats/1000').json())
    print('Ошибка запроса - строка')
    print(delete('http://127.0.0.1:8080/api/cats/b').json())
    print('Список котов до удаления')
    print(get('http://127.0.0.1:8080/api/cats').json())
    print('Успешное удаление')
    print(delete('http://127.0.0.1:8080/api/cats/2').json())
    print('Список котов после удаления')
    print(get('http://127.0.0.1:8080/api/cats').json())


def test_refactor():
    print('Ошибка запроса - попытка изменения id')
    print(put('http://127.0.0.1:8080/api/cats/1', json={'id': 4}).json())
    print('Ошибка запроса - несуществующий приют')
    print(put('http://127.0.0.1:8080/api/cats/2', json={'shelter_id': 1000}).json())
    print('Список котов до изменения')
    print(get('http://127.0.0.1:8080/api/cats').json())
    print('Успешное изменение')
    print(put('http://127.0.0.1:8080/api/cats/2', json={'name': 'Не Барсик', 'shelter_id': 1}).json())
    print('Список котов после изменения')
    print(get('http://127.0.0.1:8080/api/cats').json())


def test_validated():
    print(post('http://127.0.0.1:8080/api/cats', json={'name': 'Барсик',
                                                       'shelter_id': 3}).json())


if __name__ == '__main__':
    test_get()
    test_add()
    test_refactor()
    test_delete()
    test_validated()
    test_get()

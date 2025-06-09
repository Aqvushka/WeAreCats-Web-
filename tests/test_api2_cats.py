from requests import get, post, delete

print(get('http://localhost:8080/api/v2/cats').json())
print(get('http://localhost:8080/api/v2/cats/1').json())
print(get('http://localhost:8080/api/v2/cats/999').json())
print(post('http://localhost:8080/api/v2/cats').json())
print(post('http://localhost:8080/api/v2/cats',
           json={'name': 'Кисик'}).json())
print(post('http://localhost:8080/api/v2/cats',
           json={'name': 'Кисик', 'age': 10, 'shelters_id': 1}).json())
print('Список после добавления:')
print(get('http://localhost:8080/api/v2/cats').json())
print(delete('http://localhost:8080/api/v2/cats/999').json())
print(delete('http://localhost:8080/api/v2/cats/2').json())
print('Список после удаления:')
print(get('http://localhost:8080/api/v2/cats').json())

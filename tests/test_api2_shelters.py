from requests import get, post, delete

print(get('http://localhost:8080/api/v2/shelters').json())
print(get('http://localhost:8080/api/v2/shelters/1').json())
print(get('http://localhost:8080/api/v2/shelters/999').json())
print(post('http://localhost:8080/api/v2/shelters').json())
print(post('http://localhost:8080/api/v2/shelters',
           json={'name': 'Лапки и Хвостики'}).json())
print(post('http://localhost:8080/api/v2/shelters',
           json={'name': 'Лапки и Хвостики', 'user_id': 1}).json())
print('Список после добавления:')
print(get('http://localhost:8080/api/v2/shelters').json())
print(delete('http://localhost:8080/api/v2/shelters/999').json())
print(delete('http://localhost:8080/api/v2/shelters/7').json())
print('Список после удаления:')
print(get('http://localhost:8080/api/v2/shelters').json())

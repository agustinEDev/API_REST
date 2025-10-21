import requests

url = "http://localhost:8000/usuarios"

response = requests.get(url)

if response.status_code == 200:
    user_data = response.json()
    for user in user_data:
        print(f"Name: {user['nombre']}")
else:
    print("Failed to retrieve data. Status code:", response.status_code)

put_url = "http://localhost:8000/usuarios/1"
put_data = {
    "nombre": "Juan",
    "email": "juan@email.com"
}

response = requests.put(put_url, json=put_data)

if response.status_code == 200:
    print("User updated successfully.")
else:
    print("Failed to update user. Status code:", response.status_code)

response = requests.get(url)

if response.status_code == 200:
    user_data = response.json()
    for user in user_data:
        print(f"Name: {user['nombre']}")
else:
    print("Failed to retrieve data. Status code:", response.status_code)

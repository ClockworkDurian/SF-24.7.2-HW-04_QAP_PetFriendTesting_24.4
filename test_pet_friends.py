from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os
import random
pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result

def test_get_api_key_for_invalid_email_user(email=invalid_email, password=valid_password):
    """ Проверяем что запрос api ключа с некорректным email возвращает статус 403 и в результате содержится слово Forbidden"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'Forbidden' in result

def test_get_api_key_for_invalid_pw_user(email=valid_email, password=invalid_password):
    """ Проверяем что запрос api ключа с некорректным паролем возвращает статус 403 и в результате содержится слово Forbidden"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'Forbidden' in result

def test_get_api_key_for_invalid_email_and_pw_user(email=invalid_email, password=invalid_password):
    """ Проверяем что запрос api ключа с некорректными email и паролем возвращает статус 403 и в результате содержится слово Forbidden"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'Forbidden' in result

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_get_all_pets_with_invalid_key(filter=''):
    """ Проверяем что запрос всех питомцев с некорректным api ключем не позволяет авторизоваться и не возвращает список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее изменяем ключ.
    Далее используя измененный некорректный ключ
    запрашиваем список всех питомцев и проверяем что отсутствует доступ к сайту.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key["key"] = 'a2ec228cf4702aef18f335122cbbe05d6721d8de3ba187e5fdf02f1f'
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403
    assert 'Forbidden' in result

def test_add_new_pet_with_valid_data(name='Кот Федрила', animal_type='котопуська',
                                     age='5', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_with_invalid_data_negative_age(name='Кот Бенджамина Баттона', animal_type='Лютый котяра',
                                     age='-5', pet_photo='images/cat1.jpg'):
    """Проверяем что нельзя добавить питомца с некорректными данными (отрицательный возраст)"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status != 200
    assert result['name'] == name

def test_add_new_pet_with_invalid_data_text_age(name='Неправильный Кот', animal_type='Лютый котяра',
                                     age='Эта пять', pet_photo='images/cat1.jpg'):
    """Проверяем что нельзя добавить питомца с некорректными данными (возраст задан не числом)"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status != 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Кот Федька', animal_type='котец', age=random.randint(1, 40)):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_create_new_pet_simple_with_valid_data(name='Кот Федрила Simple', animal_type='котопуська',
                                     age='5'):
    """Проверяем что можно добавить питомца (simple, без фото) с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.сreate_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_photo(pet_photo='images/P1040103.jpg'):
    """Проверяем что можно добавить фото питомца корректного формата"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список не пустой, то пробуем обновить фото питомца
    if len(my_pets['pets']) > 0:
        status, result = pf.add_new_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_add_new_invalid_pet_photo(pet_photo='images/cat1.txt'):
    """Проверяем что невозможно добавить фото питомца некорректного формата (txt)"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список не пустой, то пробуем обновить фото питомца
    if len(my_pets['pets']) > 0:
        status, result = pf.add_new_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
        assert status == 500
        assert 'Error' in result
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_add_new_toobig_pet_photo(pet_photo='images/cat2.jpg'):
    """Проверяем что невозможно добавить фото размером больше 20 Мб"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список не пустой, то пробуем обновить фото питомца
    if len(my_pets['pets']) > 0:
        status, result = pf.add_new_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
        assert status == 500
        assert 'Error' in result
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
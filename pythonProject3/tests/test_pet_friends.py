from api import PetFriends
from settings import valid_email, valid_password
import os

# код домашнего задания начинается со строки 94

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем, что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее, используя этот ключ,
    запрашиваем список всех питомцев и проверяем, что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/2314758698.jpg'):
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


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем, что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# Homework code 1
def test_create_pet_simple_with_valid_data(name='Телепузик', animal_type='собака', age='2'):
        """Проверяем, что можно добавить питомца без фото с корректными данными"""

        # Запрашиваем ключ api и сохраняем в переменую auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # Добавляем питомца
        status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name

# Homework code 2
def test_add_photo_with_valid_data(pet_photo='images/трубкозуб.jpg'):
        """Проверяем, что можно добавить фото питомца"""

        # Запрашиваем ключ api и сохраняем в переменую auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Запрашиваем список своих питомцев
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Если список не пустой, то добавляем фото питомца:
        if len(my_pets['pets']) > 0:
            # Берём id первого питомца из списка и сохраняем в переменную pet_id
            pet_id = my_pets['pets'][0]['id']
            status, result = pf.post_add_photo(auth_key, pet_id, pet_photo)

            # Сверяем полученный ответ с ожидаемым результатом
            assert status == 200
            assert result['pet_photo'] != ''

        else:
            # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
            raise Exception("There is no my pet")

# Homework code 3
def test_get_api_key_for_invalid_email(email='pupkin', password=valid_password):
        """ Проверяем запрос api ключа c невалидным email"""

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = pf.get_api_key(email, password)

        # Сверяем полученные данные с нашими ожиданиями
        assert status == 403

# Homework code 4
def test_get_api_key_for_invalid_password(email=valid_email, password='345'):
        """ Проверяем запрос api ключа c невалидным паролем"""

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = pf.get_api_key(email, password)

        # Сверяем полученные данные с нашими ожиданиями
        assert status == 403

# Homework code 5
def test_get_api_key_for_invalid_email_and_password(email='anonim@@mail.ru', password='456'):
        """ Проверяем запрос api ключа c невалидными email и паролем"""

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = pf.get_api_key(email, password)

        # Сверяем полученные данные с нашими ожиданиями
        assert status == 403

# Homework code 6
def test_create_pet_simple_with_null_data(name='', animal_type='', age=''):
        """Проверяем, что можно добавить питомца без фото с пустыми параметрами name, animal_type, age"""

        # Запрашиваем ключ api и сохраняем в переменую auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # Добавляем питомца
        status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == ''

# Homework code 7
def test_create_pet_simple_with_unreal_age(name='', animal_type='', age='99999999999999999abC'):
        """Проверяем, что можно добавить питомца без фото с нереалистичным возрастом"""

        # Запрашиваем ключ api и сохраняем в переменую auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # Добавляем питомца
        status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['age'] == '99999999999999999abC'

# Homework code 8
def test_create_pet_simple_with_invalid_key(name='Василий', animal_type='котопёс', age='3'):
        """Проверяем, что нельзя добавить питомца без фото c невалидным auth_key"""

        # Запрашиваем ключ api и сохраняем в переменную auth_key
        auth_key = {'key': '111'}

        # Добавляем питомца
        status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 403

# Homework code 9
def test_add_photo_with_wrong_format(pet_photo='images/egik.bmp'):
    """Проверяем, что можно добавить фото питомца в отличном от указанного в документации формате .bmp"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то добавляем фото питомца:
    if len(my_pets['pets']) > 0:
        # Берём id первого питомца из списка и сохраняем в переменную pet_id
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.post_add_photo(auth_key, pet_id, pet_photo)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200

    else:
        # если спиcок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pet")

# Homework code 10
def test_add_photo_with_text_file(pet_photo='images/Hello.txt'):
        """Проверяем, что нельзя передать в качестве файла с фото текстовый файл"""

        # Запрашиваем ключ api и сохраняем в переменую auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Запрашиваем список своих питомцев
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Если список не пустой, то добавляем фото питомца:
        if len(my_pets['pets']) > 0:
            # Берём id первого питомца из списка и сохраняем в переменную pet_id
            pet_id = my_pets['pets'][0]['id']
            status, result = pf.post_add_photo(auth_key, pet_id, pet_photo)

            # Сверяем полученный ответ с ожидаемым результатом
            assert status == 500

        else:
            # если спиcок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
            raise Exception("There is no my pet")
from flask import Flask, request, render_template_string
import random
import string

app = Flask(__name__)

# генерация массива из 10000 случайных сервисов
NUM_SERVICES = 1000
services = [''.join(random.choice(string.ascii_letters) for _ in range(10)) for _ in range(NUM_SERVICES)]

# случайный выбор сервиса с ключом
plain_key_service = random.choice(services)

# шифруем название сервиса с ключом (Caesar cipher с сдвигом на 3 позиции)
ciphered_key_service = ''.join(chr((ord(c) + 3) % 256) for c in plain_key_service)

# добавляем специальные сервисы
services.extend(['search_key', 'decode'])

# генерация ключа
key = "KEY{RANDOM_SERVICE_FINDER}"

# основной маршрут: стартовая точка
@app.route('/')
def index():
    return render_template_string('''
        <h1>Key Search Among Thousands</h1>
        <p>Перед вами список из 1000 случайно сгенерированных сервисов, но с ними что то не так. В одном из них лежит ключ, но вы же не собираетесь смотреть каждый из них?.. Попробуйте ИСКАТЬ КЛЮЧ, ведь это так просто.</p>
        <form method="POST" action="/select_service">
            <select name="selected_service">
                {% for service in services %}
                    <option value="{{ service }}">{{ service }}</option>
                {% endfor %}
            </select>
            <button type="submit">Отправить запрос</button>
        </form>
    ''', services=services)

# маршрут для выбора сервиса
@app.route('/select_service', methods=["POST"])
def select_service():
    selected_service = request.form.get('selected_service')
    # формируем внутренний URL для запроса
    target_url = f'/service/{selected_service}'
    try:
        response = requests.get(target_url)
        return render_template_string(f'<h1>результат запроса</h1>\n<p>{response.text}</p>')
    except Exception as e:
        return render_template_string(f'<h1>ошибка при запросе</h1>\n<p>{str(e)}</p>')

# спец. сервис для выдачи секретного ключа
@app.route(f'/service/{plain_key_service}')
def show_key():
    return render_template_string(f'<h1>Вы нашли ключ!</h1>\n<p>Ключ: {key}</p>')

# спец. сервис для помощи (search_key)
@app.route('/service/search_key')
def help():
    return render_template_string(f'<h1>ФИНИШНАЯ ПРЯМАЯ</h1>\n<p>ключ сейчас находится в сервисе: {ciphered_key_service}, но что то мне подсказывает что с ним что то не так, может стоит его ДЕКОДировать?</p>')

# спец. сервис для расшифровки названия сервиса
@app.route('/service/decode', methods=["GET", "POST"])
def decode():
    if request.method == 'POST':
        encoded_service = request.form.get('encoded_service')
        decoded_service = ''.join(chr((ord(c) - 3) % 256) for c in encoded_service)
        return render_template_string(f'<h1>декодинг</h1>\n<p>расшифрованное название сервиса: {decoded_service}</p>')
    return render_template_string('''
        <h1>Decoder Service</h1>
        <p>вставьте зашифрованное название сервиса:</p>
        <form method="POST">
            <input type="text" name="encoded_service" placeholder="введите зашифрованное название"/>
            <button type="submit">расшифровать</button>
        </form>
    ''')

# маршрут для заглушки сервисов
@app.route('/service/<service_name>')
def service_stub(service_name):
    return render_template_string(f'<h1>Сервис {service_name}</h1>\n<p>вы выбрали сервис {service_name}, но вы промахнулись, попробуйте читать, это реально просто</p>')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
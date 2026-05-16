from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs


hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети

# !!!!! Необходимо включить сервер через if __name__ == "__main__":

# ////////////////////Закомментировал изначальный код сделанный по методике занятия/////////////////////////
# class MyServer(BaseHTTPRequestHandler):
#     """
#         Специальный класс, который отвечает за
#         обработку входящих запросов от клиентов
#     """
    # def do_GET(self):
    #     """ Метод для обработки входящих GET-запросов """
    #     # Проверка работы, что был запрос GET

    #     print(f"Пришел GET запрос на путь: {self.path}")
    #     # Проверяем, если браузер запрашивает CSS-файл 'подсказал ИИ'
    #     if self.path.endswith(".css"):
    #         self.send_response(200)  # Отправка кода stat   us ответа
    #         self.send_header("Content-type", "text/css")  # Отправка браузеру: "Это стили!"
    #         self.end_headers()  # Завершение формирования заголовков ответа
    #
    #         # Удаляем начальный слэш из пути (превращаем '/css/bootstrap.min.css' в 'css/bootstrap.min.css')
    #         file_path = self.path.strip("/")
    #
    #         with open(file_path, 'r', encoding='UTF-8') as f:
    #             self.wfile.write(bytes(f.read(), "utf-8"))
    #
    #     else:
    #         # Во всех остальных случаях отдаем страницу контактов
    #         self.send_response(200)
    #         self.send_header("Content-type", "text/html")  # Отправка браузеру: "Это HTML!"
    #         self.end_headers()
    #
    #         # Открываем файл с помощью контекстного менеджера
    #         with open('contacts.html', 'r', encoding='UTF-8')as f:
    #             # Используем функцию чтения файла
    #             html_page = f.read()
    #
    #         self.wfile.write(bytes(html_page, "utf-8"))  # Тело ответа
    #
    # def do_POST(self):
    #     """ Метод для обработки входящих POST-запросов """
    #     # Проверка работы в браузере с адресом http://localhost:8080/categories.html
    #     print("!!! МЕТОД POST ВЫЗВАН !!!")
    #     # 1. Определяем длину входящих данных
    #     content_length = int(self.headers.get('Content-Length', 0))
    #     # 2. Читаем тело запроса
    #     body = self.rfile.read(content_length).decode('utf-8')
    #     # 3. Декодируем строку (превращаем 'message=hello' в словарь {'message': ['hello']})
    #     data = parse_qs(body)
    #     print(f"Данные формы: {body}")
    #
    #     # 4. Достаем конкретное поле
    #     if 'message' in data:
    #         print(f"Связка сработала! Сообщение из формы: {data['message'][0]}")
    #         message = data.get('message', [''])[0]
    #         print(f"Пользователь написал: {message}")
    #     # 5. Отправляем ответ клиенту
    #     self.send_response(200)
    #     self.send_header("Content-type", "text/html")  # На POST отвечаем текстом HTML
    #     self.end_headers()
    #     self.wfile.write(bytes("<h3>Спасибо! Сообщение получено.</h3>", "utf-8"))
    #////////////////////////////////Конец старого кода//////////////////////////////////////////////////


class MyServer(SimpleHTTPRequestHandler):
    """
      Теперь метод do_GET удален!
      SimpleHTTPRequestHandler сам перехватит GET-запросы
      и раздаст HTML и CSS файлы из папки проекта.
    """
    def do_POST(self):
        """ Метод do_POST для обработки формы """
        # Проверка работы в браузере с адресом http://localhost:8080/categories.html
        print("!!! МЕТОД POST ВЫЗВАН !!!")
        # 1. Определяем длину входящих данных
        content_length = int(self.headers.get('Content-Length', 0))
        # 2. Читаем тело запроса
        body = self.rfile.read(content_length).decode('utf-8')
        # 3. Декодируем строку (превращаем 'message=hello' в словарь {'message': ['hello']})
        data = parse_qs(body)
        print(f"Данные формы: {body}")

        # 4. Достаем конкретное поле
        message = data.get('message', [''])[0]
        email = data.get('email', [''])[0]
        username = data.get('username', [''])[0]
        if message:
            print(f"Связка сработала! Пользователь,{username} с почтой {email} написал:{message}")
        # 5. Отправляем ответ клиенту
        self.send_response(200)
        self.send_header("Content-type", "text/html")  # На POST отвечаем текстом HTML
        self.end_headers()
        self.wfile.write(bytes("<h3>Спасибо! Сообщение получено.</h3>", "utf-8"))

if __name__ == "__main__":
    # Инициализация веб-сервера, который будет по заданным параметрах в сети
    # принимать запросы и отправлять их на обработку специальному классу, который был описан выше
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Cтарт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")

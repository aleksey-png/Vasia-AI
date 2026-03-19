from gigachat import GigaChat
import time


api_key = 'MDE5Y2Y5Y2EtODA1Zi03ZjJhLTlmM2YtYWIzNzM4MGI1MTZhOjAwM2E0YTA4LTQwNDktNGY1Ni04ZjlmLTk3YzQ1ODA1NmMzMg=='

def chat_with_gigachat():
     with GigaChat(credentials=api_key, verify_ssl_certs=False) as giga:
         print('\033[35m Вася: Привет! \033[35m')

         history = []
         while True:
             user_input = input('\033[32m Вы: \033[32m')
             print('  ')
             if user_input.lower == 'exit':
                 print('чат завершён')
                 break

             history.append({'\033[32m role\033[32m':'\033[32m user\033[32m', '\033[32m content\033[32m' : user_input})

             response = giga.chat(user_input)
             assistant_reply = response.choices[0].message.content

             print(f'\033[35m Вася: {assistant_reply}\033[35m')
             print('  ')
             history.append({'role': 'assistant', 'content': assistant_reply})

             time.sleep(1)

if __name__ == '__main__':
    chat_with_gigachat()
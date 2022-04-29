
import socket
from threading import Thread
import random
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []
nicknames = []

questions = [
    "What is the Indian Wonder in the seven wonders of the world? \n a. Qutub Minar \nb. Taj Mahal \nc. Red Fort \nd. Sun Temple",
    "Who is the Father of the Nation? \na. Jawarharlal Nehru \nb. Sardar Patel \nc. Mahatma Gandhi \nd. Lal Bahadur Shastri",
    "Which is the the national animal of India? \na. Peacock \nb. Tiger \nc. Lion \nd. Sparrow"
]

answers = ['b','c','b']

print("Server has started...")

def remove_question(index):
    questions.pop(index)
    answers.pop(index)    

def broadcast(message, connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message.encode('utf-8'))
            except:
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def remove_nickname(nickname):
     if nickname in nicknames:
         nicknames.remove(nickname) 
         
def get_random_question_answer(conn):
    random_index = random.randint(0,len(questions)-1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def clientthread(conn,nickname):
    score = 0
    conn.send("Welcome to this quiz game! ".encode('utf-8'))
    conn.send("You will receive a question. The answer to that question should be one of a, b, c or d.".encode('utf-8'))
    conn.send("\nBest of Luck for the Game!\n\n".encode('utf-8'))
    index, question ,answer = get_random_question_answer(conn)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.lower == answer:
                  score +=1
                  conn.send(f'Bravo! Your score is {score}\n\n'.encode('utf-8'))
                else:
                  conn.send("Incorrect Answer! Better luck next time!\n\n".encode('utf-8'))
                remove_question(index)
                index, question, answer = get_random_question_answer(conn)
            else:
              remove(conn)
        except:
            continue    





while True:
    conn, addr = server.accept()
    conn.send("NICKNAME".encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    list_of_clients.append(conn)
    nicknames.append(nickname)
    message = '{} has joined'.format(nickname)
    print(message)
    broadcast(message,conn)
    new_thread = Thread(target= clientthread,args=(conn,nickname))
    new_thread.start()



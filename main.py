import os
import json
import random
import math
import alive_progress as p
import datetime
import multiprocessing
from pyboxen import boxen
from rich.table import Table
from pyboxen import box
import threading
import atexit
from datetime import datetime
from datetime import timedelta
import time as t


class Spinner:
    def __init__(self, message: str = '', speed: float = 0.1) -> None:
        self.message = message
        self.speed = speed
        self.stop_event = threading.Event()

        self.thread = threading.Thread(
            target=self.run_spinner,
            name='Spinner Thread'
        )

    def run_spinner(self) -> None:
        spinner_chars = ['|', '/', '-', '\\']
        n = 0
        while not self.stop_event.is_set():
            print(f'\r{self.message} {spinner_chars[n]}', end='')
            n = (n + 1) % len(spinner_chars)
            t.sleep(self.speed)

    def start_spinner(self) -> None:
        self.thread.start()

    def stop_spinner(self) -> None:
        if not self.thread.is_alive():
            raise RuntimeError('Spinner is not alive')
        self.stop_event.set()
        self.thread.join()
        print()

if __name__ == '__main__':
    spinner = Spinner('Loading', 2.5)
    spinner.start_spinner()
    t.sleep(4)
    spinner.stop_spinner()

def check_total_loss():
  loss = userProfile['total_loss']
  print(boxen(f'[red] -£{loss} [/red]', title='[red]Total Loss: [/red]'))

def check_total_won():
  won = userProfile['total_won']
  print(boxen(f'[green] +£{won} [/green]', title='[green]Total Won: [/green]'))
    
def check_total_change():
  if userProfile['total_won'] > userProfile['total_loss']:
    total = userProfile['total_won'] - userProfile['total_loss']
    print(boxen(f'[green]Your overall balance has increased by £{total}[/green]', title = 'Total Change:'))
  elif userProfile['total_won'] < userProfile['total_loss']:
    total = userProfile['total_loss'] - userProfile['total_won']
    print(boxen(f'[red]Your overall balance has decreased by £{total}[/red]', title = 'Total Change:'))
  else:
    print(boxen('Your overall balance has not changed', title = 'Total Change:'))

def send_money():
  file = open('./history_data/1' + userID + '.txt', 'a')
  file.write('[red]Sent ' + str(amount) + ' to ' + sentTo['user_id'] +
             '[/red] - ')
  file.write(str(datetime.now()))
  file.write('\n')
  file.close()
  file = open('./history_data/1' + sentTo['user_id'] + '.txt', 'a')
  file.write('[green]Recieved ' + str(amount) + ' from ' + userID +
             '[/green] - ')
  file.write(str(datetime.now()))
  file.write('\n')
  file.close()


def add_win():
  with open('data.json', 'w') as f:
    userProfile['total_won'] = userProfile['total_won'] + won
    json.dump(data, f)
  file = open('./history_data/1' + userID + '.txt', 'a')
  file.write('[green]Won ' + str(won) + ' from ' + game + '[/green] - ')
  file.write(str(datetime.now()))
  file.write('\n')
  file.close()


def add_loss():
  with open('data.json', 'w') as f:
    userProfile['total_loss'] = userProfile['total_loss'] + gamble
    json.dump(data, f)
  num = random.randint(1,6)
  if num == 1:
    print('So close, better luck next time!')
  elif num == 2:
    print('Only 3 tries away from winning!')
  elif num == 3:
    print('You can do better than that!')
  elif num == 4:
    print('I can feel a jackpot coming your way!')
  elif num == 5:
    print('Only a few spins away!')
  elif num == 6:
    print('Almost time for a jackpot!')
  file = open('./history_data/1' + userID + '.txt', 'a')
  file.write('[red]Lost ' + str(gamble) + ' from ' + game + '[/red] - ')
  file.write(str(datetime.now()))
  file.write('\n')
  file.close()


def check_history():
  global table
  file = open('./history_data/1' + userID + '.txt', 'r')
  history = file.read()
  if history == '':
    print('No history to show')
  else:
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("History", width=35)
    table.add_column("Date")
    temp = history.split('\n')
    for item in temp:
      parts = item.split(' ')
      if len(parts) >= 4:
        balance = int(parts[1].replace(',', '').replace('£', ''))
        sender = parts[3]
        date = ' '.join(parts[5:7])
        table.add_row(
            parts[0] + ' £{:,}'.format(balance) + ' ' + parts[2] + ' ' +
            sender, date)
    print(boxen(table))
    file.close()


def add_history():
  file_path = './history_data/1' + newUserID + '.txt'
  file = open(file_path, 'w')
  file.close()

MAX_LINES = 3
MAX_BET = 100000000000000
MIN_BET = 10

symbol_count = {
  '£': 2,
  '/': 4,
  '7': 6,
  '$': 8
}

symbol_value = {
  '£': 5,
  '/': 4,
  '7': 3,
  '$': 2
}

def check_won(columns, lines, gamble, values):
  global lose
  lose = True
  global won
  won = 0
  winning_lines = []
  for line in range(lines):
    symbol = columns[0][line]
    for column in columns:
      symbol_to_check = column[line]
      if symbol != symbol_to_check:
        userProfile['balance'] = userProfile['balance'] - gamble
        bankProfile['balance'] = bankProfile['balance'] + gamble
        lose = True
        break
    else:
      won += values[symbol] * gamble
      userProfile['balance'] = userProfile['balance'] + won
      bankProfile['balance'] = bankProfile['balance'] - won
      winning_lines.append(line + 1)
      lose = False
  return won, winning_lines



def get_slot_machine_spin(rows, cols, symbols):
  all_symbols = []
  for symbol, symbol_count in symbols.items():
    for _ in range(symbol_count):
      all_symbols.append(symbol)

  columns = []
  for _ in range(cols):
    column = []
    current_symbols = all_symbols[:]
    for _ in range(rows):
      value = random.choice(current_symbols)
      current_symbols.remove(value)
      column.append(value)

    columns.append(column)

  return columns

def print_slot_machine(columns):
  for row in range(len(columns[0])):
    for i, column in enumerate(columns):
      if i != len(columns) - 1:
        print(column[row], end = ' | ')
      else:
        print(column[row], end = '')

    print()


def get_lines():
  while True:
    print(boxen(f'(1-{MAX_LINES})', title = 'Number of lines to bet on '))
    lines = input('Enter option: ')
    if lines.isdigit():
      lines = int(lines)
      if 1 <= lines <= MAX_LINES:
        break
      else:
        print(boxen(f'Number of lines must be between 1 and {MAX_LINES}', title = '[red] [ERROR] [/red]'))
        t.sleep(0.5)
    else:
        print('Please enter a number.')
  return lines

def get_gamble():
  while True:
    amount = input('What do you want to gamble on each line? £')
    if amount.isdigit():
      amount = int(amount)
      if amount <= userProfile['balance']:
        if MIN_BET <= amount <= MAX_BET:
          break
        else:
          print(f'Amount must be between £{MIN_BET}- £{MAX_BET}.')
      else:
        print('You don\'t have that much to gamble.')
        print('Your balance is £' + str(userProfile['balance']) + '.')
    else:
        print('Please enter a valid number.')
  return amount

def slotMachineRun():
  global gamble
  global game
  global confirmed
  confirmed = True
  game = 'Slots'
  lines = get_lines()
  while True:
    money = get_gamble()
    gamble = money * lines
    if gamble > userProfile['balance']:
      print('You don\'t have enough to gamble that amount')
      print('Current balance is £' + str(userProfile['balance']) + '.')
    else:
      break
  print(f'You are gambling £{money} on {lines} lines.')
  print(f'Total gamble is £{gamble}.')
  if __name__ == '__main__':
    spinner = Spinner('Loading...', 0.2)
    spinner.start_spinner()
    t.sleep(10)
    spinner.stop_spinner()
    slots = get_slot_machine_spin(3, 3, symbol_count)
    print_slot_machine(slots)
    won, winning_lines = check_won(slots, lines, gamble, symbol_value)
    print(f'You won £{won}.')
    print(f'You won on {winning_lines} lines:')
    userProfile['balance'] = userProfile['balance'] +  won 
  else:
    print('Please enter a valid option.')


## works
def display_leaderboard():
  with open('data.json') as f:
    newLeaderData = json.load(f)
  sorted_leaderboard = sorted(newLeaderData['user_data'], key=lambda x: x['balance'], reverse=True)
  table = Table(show_header=True, header_style="bold magenta")
  table.add_column("Place", width=5)
  table.add_column("User", width=40)
  table.add_column("Balance")
  for index, entry in enumerate(sorted_leaderboard, start=0):
    if entry['user_id'] == 'test':
      continue
    table.add_row(str(index), entry['user_id'], '£{:,}'.format(entry['balance']))

  print(boxen(table))
  


## works 
def show_leaderboard():
  with open('data.json') as f:
    newLeaderData = json.load(f)
  end = datetime.now()
  totalTime = int((end - start).total_seconds())
  sorted_leaderboard = sorted(newLeaderData['user_data'], key=lambda y: y["time_played"], reverse=True)
  table = Table(show_header=True, header_style="bold magenta")
  table.add_column("Place", width=5)
  table.add_column("User", width=45)
  table.add_column("Total Time Played")
  for index, entry in enumerate(sorted_leaderboard, start=0):
    if entry['user_id'] == userID:    
      totalTimePlayed = totalTime + entry['time_played']
    else:
      totalTimePlayed = entry['time_played']
    if entry['user_id'] == "test":
        continue
    table.add_row(str(index), entry["user_id"], str(timedelta(seconds=totalTimePlayed)))

  print(boxen(table))



with open('data.json') as f:
  data = json.load(f)

userProfile = ''
bankProfile = data['bank_data'][0]


def LogIn():
  global userID
  global userProfile
  global newUserID
  userProfile = ''
  newUserID = ''
  newUserPass = ''
  found = False
  sameID = True
  makingNewUser = False
  passwordCorrect = False
  commandFound = False
  while not commandFound:
    print(
        boxen('(1) Log in\n(2) Sign up\n(3) Exit',
              title='What do you want to do?'))
    menuOption = input('Enter Option: ')
    if menuOption == '1':
      commandFound = True
      while not found:
        userID = input('Input your ID: ')
        for userProfile in data['user_data']:
          if userProfile['user_id'] == userID:
            found = True
            while not passwordCorrect:
              passwordCheck = input('Please input your password: ')
              if passwordCheck == userProfile['password']:
                passwordCheck = True
                sameID = False
                return
              else:
                print('Incorrect password')
        print('ID is incorrect try again')
    elif menuOption == '2':
      commandFound = True
      while sameID == True:
        if not found:
          newUserID = input('Enter ID for your User: ')
          newUserPass = input('Enter your password: ')
          for userProfile in data['user_data']:
            if userProfile['user_id'] == newUserID:
              print('ID already exists. Please choose a different one.')
              sameID = True
              break
            else:
              sameID = False
              makingNewUser = True
              found = True
              break

    if makingNewUser == True:
      new_user_profile = {
          'user_id': newUserID,
          "password": newUserPass,
          "balance": 50,
          "time_played": 0, 
          'total_loss': 0,
          'total_won': 0
      }
      bankProfile['balance'] = bankProfile['balance'] - 50
      data['user_data'].append(new_user_profile)
      print("New profile added:", new_user_profile)
      with open('data.json', 'w') as f:
        json.dump(data, f)
      userProfile = new_user_profile
      userID = newUserID
      add_history()
      return userProfile
    elif menuOption == '3':
      exit()
    else:
      print('[ERROR] Command not found. Please try again.')


LogIn()
start = datetime.now()
print('Welcome', userProfile['user_id'])

playing = False
while not playing:
  global won
  global gamble

  print(boxen(
          '(0) Check transaction history\n(1) Sign out\n(2) Change password\n(3) Check balance\n(4) Slots\n(5) Roulette\n(6) Gift Money\n(7) Time Played\n(8) Check Money Leaderboard\n(9) Check Time Played Leaderboard\n(10) Check Bank\n(11) Check Total Won\n(12) Check Total Lost\n(13) Check Overall Change')) 
  title=('What do you want to do?')
  choice = input('Enter option: ')

  if choice == "4":
    end = datetime.now()
    totalTime = int((end - start).total_seconds())
    userProfile['time_played'] = userProfile['time_played'] + int(totalTime)
    with open('data.json', 'w') as f:
      json.dump(data, f)
    slotMachineRun()
    if lose == True:
      add_loss()
    if lose == False:
      add_win()
  elif choice == '11':
    check_total_won()
  elif choice == '12':
    check_total_loss()
  elif choice == '13':
    check_total_change()
  elif choice == "5":
    end = datetime.now()
    totalTime = int((end - start).total_seconds())
    userProfile['time_played'] = userProfile['time_played'] + int(totalTime)
    with open('data.json', 'w') as f:
      json.dump(data, f)
    game = 'Roulette'
    gamble = int(input("How much do you want to gamble? £"))
    if gamble > userProfile['balance']:
      print("You haven\'t got that much to gamble")
    else:
      print(boxen('(1) Number\n(2) Colour', title='Number or colour?'))
      skibidi = input('Enter Option: ')
      if skibidi == '1':
        print(boxen('0 - 36', title='Pick a number '))
        num = int(input('Enter option: '))

        class RouletteTable:
          global won

          def __init__(self):
            self.numbers = list(range(0, 37))  # 0 to 36
            self.colors = {
                0: 'green',
                1: 'red',
                2: 'black',
                3: 'red',
                4: 'black',
                5: 'red',
                6: 'black',
                7: 'red',
                8: 'black',
                9: 'red',
                10: 'black',
                11: 'black',
                12: 'red',
                13: 'black',
                14: 'red',
                15: 'black',
                16: 'red',
                17: 'black',
                18: 'red',
                19: 'red',
                20: 'black',
                21: 'red',
                22: 'black',
                23: 'red',
                24: 'black',
                25: 'red',
                26: 'black',
                27: 'red',
                28: 'black',
                29: 'black',
                30: 'red',
                31: 'black',
                32: 'red',
                33: 'black',
                34: 'red',
                35: 'black',
                36: 'red'
            }

          def spin(self):
            return random.choice(self.numbers)

          def get_color(self, number):
            return self.colors[number]

        if __name__ == "__main__":
          roulette = RouletteTable()
          winning_number = roulette.spin()
          if __name__ == '__main__':
            spinner = Spinner('Loading...', 0.2)
            spinner.start_spinner()
            t.sleep(6)
            spinner.stop_spinner()
          print("Winning number is:", winning_number)
          t.sleep(0.5)
          print("Color of the winning number is:",
                roulette.get_color(winning_number))

        if num == winning_number:
          t.sleep(0.5)
          add_win()
          print("Well done. You won!")
          won = int(gamble * 2)
          bankProfile['balance'] = bankProfile['balance'] - won
          userProfile['balance'] = userProfile['balance'] + won
          t.sleep(0.5)
          print('New Balance is £', userProfile['balance'])
          for user_data in data['user_data']:
            if user_data['user_id'] == userProfile['user_id']:
              user_data['balance'] = userProfile['balance']
          with open('data.json', 'w') as f:
            json.dump(data, f)
        else:
          t.sleep(0.5)
          add_loss()
          userProfile['balance'] = userProfile['balance'] - gamble
          bankProfile['balance'] = bankProfile['balance'] + gamble
          t.sleep(0.5)
          print('Your balance is now £', userProfile['balance'])
          with open('data.json', 'w') as f:
            json.dump(data, f)

      elif skibidi == '2':
        print(
            boxen('[red](1) Red[/red]\n[black](2) Black[/black]', title='Pick a colour?'))
        colour = input('Enter Option: ')

        class RouletteTable:

          def __init__(self):
            self.numbers = list(range(0, 37))  # 0 to 36
            self.colors = {
                0: 'green',
                1: 'red',
                2: 'black',
                3: 'red',
                4: 'black',
                5: 'red',
                6: 'black',
                7: 'red',
                8: 'black',
                9: 'red',
                10: 'black',
                11: 'black',
                12: 'red',
                13: 'black',
                14: 'red',
                15: 'black',
                16: 'red',
                17: 'black',
                18: 'red',
                19: 'red',
                20: 'black',
                21: 'red',
                22: 'black',
                23: 'red',
                24: 'black',
                25: 'red',
                26: 'black',
                27: 'red',
                28: 'black',
                29: 'black',
                30: 'red',
                31: 'black',
                32: 'red',
                33: 'black',
                34: 'red',
                35: 'black',
                36: 'red'
            }

          def spin(self):
            return random.choice(self.numbers)

          def get_color(self, number):
            return self.colors[number]

        if __name__ == "__main__":
          roulette = RouletteTable()
          winning_number = roulette.spin()
          if __name__ == '__main__':
            spinner = Spinner('Loading...', 0.2)
            spinner.start_spinner()
            t.sleep(6)
            spinner.stop_spinner()
          print("Winning number is:", winning_number)
          t.sleep(0.5)
          print("Color of the winning number is:",
                roulette.get_color(winning_number))
          winning_colour = roulette.get_color(winning_number)

        if colour == '1' and winning_colour == 'red' or colour == '2' and winning_colour == 'black':
          t.sleep(0.5)
          print("Well done. You won!")
          won = int(gamble * 1.5)
          bankProfile['balance'] = bankProfile['balance'] - won
          add_win()
          userProfile['balance'] = userProfile['balance'] + won
          t.sleep(0.5)
          print('New Balance is £', userProfile['balance'])
          for user_data in data['user_data']:
            if user_data['user_id'] == userProfile['user_id']:
              user_data['balance'] = userProfile['balance']
          with open('data.json', 'w') as f:
            json.dump(data, f)
        else:
          t.sleep(0.5)
          add_loss()
          userProfile['balance'] = userProfile['balance'] - gamble
          bankProfile['balance'] = bankProfile['balance'] + gamble
          t.sleep(0.5)
          print('Your balance is now £', userProfile['balance'])
          with open('data.json', 'w') as f:
            json.dump(data, f)

  elif choice == "3":
    end = datetime.now()
    totalTime = int((end - start).total_seconds())
    userProfile['time_played'] = userProfile['time_played'] + int(totalTime)
    with open('data.json', 'w') as f:
      json.dump(data, f)
    print('Loading balance...')
    with p.alive_bar(100) as bar:
      for _ in range(100):
        t.sleep(0.0075)
        bar()
    print(boxen('[magenta]Your balance is - £{:,} [/magenta]'.format(userProfile['balance'])))
  elif choice == "ADD":
    end = datetime.now()
    totalTime = int((end - start).total_seconds())
    userProfile['time_played'] = userProfile['time_played'] + int(totalTime)
    with open('data.json', 'w') as f:
      json.dump(data, f)
    addAmount = int(input('How much do you want to add to your account? '))
    userProfile['balance'] = userProfile['balance'] + addAmount
    for user_data in data['user_data']:
      if user_data['user_id'] == userProfile['user_id']:
        user_data['balance'] = userProfile['balance']
    with open('data.json', 'w') as f:
      json.dump(data, f)

  elif choice == "1":
    end = datetime.now()
    totalTime = int((end - start).total_seconds())
    userProfile['time_played'] = userProfile['time_played'] + int(totalTime)
    with open('data.json', 'w') as f:
      json.dump(data, f)
    print("Signed out succesfully.\nGoodbye")
    LogIn()

  elif choice == "2":
    end = datetime.now()
    totalTime = int((end - start).total_seconds())
    userProfile['time_played'] = userProfile['time_played'] + int(totalTime)
    with open('data.json', 'w') as f:
      json.dump(data, f)
    old_pass = input('Enter your old password: ')
    if old_pass == userProfile['password']:
      new_pass = input('Enter your new password: ')
      confirm = input('Confirm your new password: ')
      if confirm == new_pass:
        print('Password successfully changed to', new_pass)
        userProfile['password'] = new_pass
        with open('data.json', 'w') as f:
          json.dump(data, f)
      else:
        print('Passwords do not match')
    else:
      print('Incorrect password')

  elif choice == "0":
    end = datetime.now()
    totalTime = int((end - start).total_seconds())
    userProfile['time_played'] = userProfile['time_played'] + int(totalTime)
    with open('data.json', 'w') as f:
      json.dump(data, f)
    check_history()
  elif choice == "6":
    end = datetime.now()
    totalTime = int((end - start).total_seconds())
    userProfile['time_played'] = userProfile['time_played'] + int(totalTime)
    with open('data.json', 'w') as f:
      json.dump(data, f)
    global sentTo
    global amount
    sentTo = input('Enter the ID of the user you want to send money to: ')
    amount = int(input('Enter the amount you want to send: '))
    if amount > int(userProfile['balance']):
      print('You don\'t have that much money')
    else:
      for tempUser in data['user_data']:
        if tempUser['user_id'] == sentTo:
          tempUser['balance'] = tempUser['balance'] + amount
          userProfile['balance'] = userProfile['balance'] - amount
          with open('data.json', 'w') as f:
            json.dump(data, f)
          print(
              boxen('Your balance is - £{:,}'.format(userProfile['balance']),
                    color='green',
                    title='[green] £{:,}'.format(
                        (amount)) + ' Sent to  user![/green] '))
          sentTo = tempUser
          send_money()
          break
      else:
        print('The UserID ' + sentTo + ' doesn\'t exist. Please try again.')
  elif choice == "10":
      print('The Bank of Kockfoster has £{:,}'.format(bankProfile['balance']))
  elif choice == "7":
    end = datetime.now()
    totalTime = int((end - start).total_seconds())
    userProfile['time_played'] = userProfile['time_played'] + int(totalTime)
    with open('data.json', 'w') as f:
      json.dump(data, f)
    with open('data.json', 'r') as f:
      data = json.load(f)
      time_played = userProfile['time_played']
      days = time_played // 86400
      hours = (time_played % 86400) // 3600
      minutes = (time_played % 3600) // 60
      seconds = time_played % 60
      days = ('{:,}'.format(days))
      print(f'You have gambled for a total of {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds')
  elif choice == "8":
    end = datetime.now()
    totalTime = int((end - start).total_seconds())
    userProfile['time_played'] = userProfile['time_played'] + int(totalTime)
    with open('data.json', 'w') as f:
      json.dump(data, f)
    display_leaderboard()
  elif choice == '9':
    show_leaderboard()
  else:
    end = datetime.now()
    totalTime = int((end - start).total_seconds())
    userProfile['time_played'] = userProfile['time_played'] + int(totalTime)
    with open('data.json', 'w') as f:
      json.dump(data, f)
    print('[ERROR] That command isn\'t valid.')


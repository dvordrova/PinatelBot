import threading
from datetime import date
from automata.state_abstract import *
import config
from collections import defaultdict

class User:
    # delay = 30 if config.LOCAL else 60 * 30
    delay = 60 * 30
    TASK_ANSWERS = {
        'Дела': 'Молодец! Продолжай в том же духе!',
        'Отдых': 'Отдыхай, отдыхай ;3',
        'Проёб': 'Бля, не проёбывайся!',
        'Ежедневная хуйня': 'Понимаю'
    }

    def __init__(self, bot, id):
        self.bot = bot
        self.id = id
        self.today = defaultdict(list)
        self.daily = ['ем', 'завтрак', 'обед', 'ужин', 'туалет', 'еду', 'иду', 'жду']
        self.state = SleepingState(id)
        self.done_jobs = set()
        threading.Timer(self.delay, self.timer).start()


    def timer(self):
        if isinstance(self.state, TimerState):
            self.state.next_step()
        threading.Timer(self.delay, self.timer).start()

    def update(self, text):
        text = text.lower()
        new_state, d = self.state.next_step(text)
        if isinstance(self.state, ListCreatorState) and d:
            self.today.update(d)
        if isinstance(self.state, TimerState) and isinstance(new_state, TimerState):
            struct = State._get_struct(text)
            type = 'Проёб'
            for key, item in self.today.items():
                for task, s in item:
                    if s == struct:
                        type = key
                        if key == 'Дела':
                            self.done_jobs.add(task)
            if type == 'Проёб':
                for routine in self.daily:
                    if routine in text:
                        type = 'Ежедневная хуйня'
            self.state.send(self.TASK_ANSWERS[type])
            if type != 'Дела':
                undone_jobs = [job[0] for job in self.today['Дела'] if job[0] not in self.done_jobs]
                if undone_jobs:
                    self.state.send('Не забывай про следующие дела:\n - {}'.format('\n - '.join(undone_jobs)))
                else:
                    self.state.send('Но в принципе все дела сделаны)\nВсегда можешь добавить еще дел при помощи комманды /add')

        self.state = new_state
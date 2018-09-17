import pymorphy2
import telebot
from typing import Tuple, Any, List, Optional
from random import choice

class State:
    bot = None
    morph = pymorphy2.MorphAnalyzer()

    def __init__(self, chat_id):
        if not State.bot:
            raise RuntimeError('Please initialize State.bot inside main')
        self.chat_id = chat_id

    def send(self, msg: str):
        self.bot.send_message(self.chat_id, msg)

    def next_step(self, answer: str) -> Tuple[object, Optional[List]]:
        raise NotImplemented

    @staticmethod
    def _get_struct(s: str) -> str:
        return ' '.join(sorted(State.morph.parse(word)[0].normal_form
                        for word in ''.join(c if str.isalpha(c) else ' '
                                            for c in s
                                           ).split()
                              )
                       )

class SleepingState(State):
    KEYWORDS = ('утро',
                'утречка',
                'утра',
                'доброго нарут',
                'доброго борут',
                'бобречка',
               )
    ANSWERS = ('Утречка)',
               'Доброго утра!',
               'Хуютра'
              )

    def __init__(self, chat_id: int):
        super().__init__(chat_id)
        self.list = list()
        self.next_state = ListCreatorState(chat_id, 'Какие дела тебя ждут сегодня?', 'Дела',
                          ListCreatorState(chat_id, 'Какой отдых тебя сегодня ожидает?', 'Отдых',
                          TimerState(chat_id)))

    def next_step(self, answer: str):
        if any(key.lower() in answer.lower() for key in self.KEYWORDS):
            self.send(choice(self.ANSWERS))
            self.next_state.next_step()
            return self.next_state, None
        else:
            self.send('...zzZZZ')
            return self, None


class TimerState(State):
    SLEEP_KEYS = ('Спокойной ночи', 'Снов', 'Сладких снов', 'Приятных снов', 'Спяй', 'Споки')

    def __init__(self, chat_id):
        super().__init__(chat_id)

    def next_step(self, answer: str = ''):
        if any(key.lower() in answer.lower() for key in self.SLEEP_KEYS):
            self.send('{}\nЖду тебя завтра:3'.format(choice(self.SLEEP_KEYS)))
            return SleepingState(self.chat_id), None
        if not answer:
            self.send('Что делаешь?')
        return self, None



class ListCreatorState(State):
    def __init__(self, chat_id: int, msg: str, list_identifier: str, next_state: State):
        super().__init__(chat_id)
        self.msg = msg
        self.list = list()
        self.list_identifier = list_identifier
        self.next_state = next_state

    def next_step(self, answer: str = '') -> Tuple[State, Optional[dict]]:
        answer = answer.lower()
        if answer.strip():
            answer_structure = self._get_struct(answer)
            if answer_structure.lower() == 'нет':
                if self.list:
                    self.send('{}:\n - {}'.format(self.list_identifier, '\n - '.join(a[0] for a in self.list)))
                if isinstance(self.next_state, ListCreatorState):
                    self.next_state.next_step()
                else:
                    self.send('Понял тебя, иди делай дела)')
                return self.next_state, {self.list_identifier: self.list}
            else:
                for line_a in answer.splitlines():
                    self.list.append((line_a, self._get_struct(line_a)))
                self.send('Хочешь добавить в этот список что-нибудь еще?')
                return self, None
        else:
            self.send(self.msg)

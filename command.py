import pymorphy2


class Command:
    morph = pymorphy2.MorphAnalyzer()

    @staticmethod
    def _get_struct(s):
        return ' '.join(sorted(Command.morph.parse(word)[0].normal_form
                      for word in ''.join(c if str.isalpha(c) else ' '
                                          for c in s
                                         ).split()
                     )
                        )

    def __init__(self, names):
        self.abbs = {name:self._get_struct(name) for name in names}

    def is_command(self, s):
        pass
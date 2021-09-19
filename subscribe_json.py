import os.path
import json


class SubscribeJson:

    __slots__ = {"data", "filename"}

    def __init__(self, filename='subscribers.json'):
        self.data = {}
        self.filename = filename
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                self.data = json.loads(f.read())

    def items(self):
        return self.data.items()

    def subscribe(self, chat_id, username):
        self.data[chat_id] = username
        self._save_to_file()

    def unsubscribe(self, chat_id):
        self.data.pop(chat_id)
        self._save_to_file()

    def _save_to_file(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.data, indent=2, ensure_ascii=False))

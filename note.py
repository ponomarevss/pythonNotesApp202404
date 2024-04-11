class Note:
    def __init__(self, note_id, header, body, timestamp):
        self.note_id = note_id
        self.header = header
        self.body = body
        self.timestamp = timestamp

    def __str__(self):
        return f"ID: {self.note_id}\nHeader: {self.header}\nBody: {self.body}\nTimestamp: {self.timestamp}"

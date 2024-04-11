import csv
import datetime
import os

from note import Note


class StorageHandler:
    def __init__(self):
        self.STORAGE_FILE = "storage.csv"

    def save_notes_list_to_csv(self, notes_list):
        with open(self.STORAGE_FILE, mode="w", newline="") as file:
            writer = csv.writer(file, delimiter=';')
            for note in notes_list:
                writer.writerow([note.note_id, note.header, note.body, note.timestamp])

    def read_notes_from_csv(self):
        notes = []
        if os.path.isfile(self.STORAGE_FILE):
            with open(self.STORAGE_FILE, mode="r") as file:
                reader = csv.reader(file, delimiter=';')
                for row in reader:
                    note_id, header, body, timestamp_str = row
                    timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
                    notes.append(Note(int(note_id), header, body, timestamp))
        return notes

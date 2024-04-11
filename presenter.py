import calendar
import datetime
from operator import attrgetter

from note import Note
from storage_handler import StorageHandler
from view import View


class Presenter:

    def __init__(self, view=View(), storage_handler=StorageHandler()):
        self._view = view
        self._storage_handler = storage_handler
        self._notes_list = self._storage_handler.read_notes_from_csv()

    def create_new_note(self):
        note_id = 0 if len(self._notes_list) == 0 else self._notes_list[-1].note_id + 1
        header = self._view.get("Input header: ")
        body = self._view.get("Input body: ")
        timestamp = datetime.datetime.now()
        new_note = Note(note_id=note_id, header=header, body=body, timestamp=timestamp)

        self._notes_list.append(new_note)
        self._storage_handler.save_notes_list_to_csv(self._notes_list)
        self._view.set(f"Note saved with ID={new_note.note_id} and timestamp={new_note.timestamp}")

    def edit_note(self):
        pending_note = self._get_note_by_id()
        if pending_note is None:
            self._view.set("No note with such ID.\n")
            return
        self._view.set(f"ID: {pending_note.note_id} | Timestamp: {pending_note.timestamp}\n"
                       f"{pending_note.header}\n{pending_note.body}\n")
        choice = None
        while choice != 9:
            choice = self.get_constrained_int(
                'Options: 1. Edit header, 2. Edit body, 3. Delete, 9. Main menu\n',
                1, 9)
            if choice == 1:
                pending_note.header = self._view.get('Input new header: ')
                pending_note.timestamp = datetime.datetime.now()
                self._storage_handler.save_notes_list_to_csv(self._notes_list)
            elif choice == 2:
                pending_note.body = self._view.get('Input new body: ')
                pending_note.timestamp = datetime.datetime.now()
                self._storage_handler.save_notes_list_to_csv(self._notes_list)
            elif choice == 3:
                self._notes_list.remove(pending_note)
                self._storage_handler.save_notes_list_to_csv(self._notes_list)
                self._view.set('Pending note deleted')
                return

    def show_all_notes(self):
        notes_list = sorted(self._notes_list, key=attrgetter("timestamp"))
        self._show_notes(notes_list)

    def show_notes_in_datetime_range(self):
        start_date = self._get_date("Set start datetime.")
        end_date = self._get_date("Set end datetime.")

        sorted_list = sorted(self._notes_list, key=attrgetter("timestamp"))
        filtered_list = filter(lambda note: start_date <= note.timestamp <= end_date, sorted_list)
        self._show_notes(filtered_list)

    def get_constrained_int(self, invitation, min_constraint, max_constraint):
        result = None
        while result is None:
            try:
                user_input = int(self._view.get(invitation))
                if user_input in range(min_constraint, max_constraint + 1):
                    result = user_input
                else:
                    self._view.set(f"Invalid input. Integer must be within {min_constraint} .. {max_constraint}.")
            except ValueError:
                self._view.set("Invalid input. Please enter an integer.")
        return result

    def _get_note_by_id(self):
        note_id = self._get_int("Input ID: ")
        for note in self._notes_list:
            if note.note_id == note_id:
                return note
        return None

    def _show_notes(self, notes):
        for note in notes:
            self._view.set(f"{note.note_id:10} | {note.header:50} | {note.timestamp}")

    def _get_int(self, invitation):
        user_input = None
        while user_input is None:
            try:
                user_input = int(self._view.get(invitation))
            except ValueError:
                self._view.set("Invalid input. Please enter an integer.")
        return user_input

    def _get_year(self):
        return self.get_constrained_int("Input year: ", datetime.MINYEAR, datetime.MAXYEAR)

    def _get_month(self):
        return self.get_constrained_int("Input month: ", 1, 12)

    def _get_day(self, year, month):
        mum_days = calendar.monthrange(year, month)[1]
        return self.get_constrained_int("Input day: ", 1, mum_days)

    def _get_date(self, invitation):
        self._view.set(invitation)
        year = self._get_year()
        month = self._get_month()
        day = self._get_day(year, month)
        return datetime.datetime(year, month, day)

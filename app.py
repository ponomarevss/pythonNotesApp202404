from presenter import Presenter


class App:

    def __init__(self):
        self.presenter = Presenter()

    def start(self):
        choice = None
        while choice != 9:
            choice = self.presenter.get_constrained_int(
                'Main menu: 1. Add note, 2. Edit note, 3. Show all, 4. Show within range, 9. Quit\n',
                1, 9)
            if choice == 1:
                self.presenter.create_new_note()
            elif choice == 2:
                self.presenter.edit_note()
            elif choice == 3:
                self.presenter.show_all_notes()
            elif choice == 4:
                self.presenter.show_notes_in_datetime_range()

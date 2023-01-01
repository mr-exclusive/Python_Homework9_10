import os


class Phonebook:
    def __init__(self):
        self.contacts = list()
        self.file_name = 'contacts_db.csv'

    def read_contacts(self):
        if os.path.isfile(self.file_name):
            if os.stat(self.file_name).st_size != 0:
                with open(self.file_name, "r", encoding="utf_8") as f:
                    self.contacts = list(map(lambda x: x.split(','), f.read().split('\n')))

    def save_contacts(self):
        if len(self.contacts) > 0:
            with open(self.file_name, "w", encoding="utf_8") as f:
                f.write('\n'.join([','.join(contact) for contact in self.contacts]))
        else:
            if os.path.isfile(self.file_name):
                if os.stat(self.file_name).st_size != 0:
                    os.remove(self.file_name)

    def add_contact(self, raw_contact):
        if raw_contact:
            parts = raw_contact.split(',')
            if len(parts) > 1:
                contact = [parts[0].strip(), parts[1].strip()]  # 0-name; 1-phone
                self.contacts.append(contact)
                return True

        return False

    def print_contacts(self):
        if len(self.contacts) == 0:
            return '(empty)'
        else:
            result = ''
            for i, contact in enumerate(self.contacts, start=1):
                result += f'{i}. {": ".join(contact)}\n'
            return result

    def search_contacts(self, search_string):
        found_contacts = [contact for contact in self.contacts if search_string in contact[0]]

        if len(found_contacts) == 0:
            return '(no results)'
        else:
            result = f'Found {len(found_contacts)} contact(s):\n'
            for contact in found_contacts:
                result += f'# {": ".join(contact)}\n'
            return result

    def delete_contact(self, msg):
        if msg:
            if msg.isdigit():
                contact_id = int(msg)
                if 0 < contact_id <= len(self.contacts):
                    del self.contacts[contact_id-1]
                    return True

        return False

    def perform_command(self, command):
        if command == 'Show':
            return self.print_contacts()
        else:
            return 'Unknown command!'

import unittest

import app
from app import (add_new_doc, add_new_shelf, append_doc_to_shelf,
                 check_document_existance, delete_doc,
                 get_all_doc_owners_names, get_doc_owner_name, get_doc_shelf,
                 move_doc_to_shelf, remove_doc_from_shelf, show_all_docs_info,
                 show_document_info)


class TestSecretaryProgram(unittest.TestCase):

    def setUp(self):
        """Сбрасываем данные в модуле app"""
        app.documents = [
            {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
            {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
            {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
        ]
        app.directories = {
            '1': ['2207 876234', '11-2'],
            '2': ['10006'],
            '3': []
        }

    def test_check_document_existance(self):
        self.assertTrue(check_document_existance("11-2"))
        self.assertFalse(check_document_existance("999"))

    def test_get_doc_owner_name(self):
        self.assertEqual(get_doc_owner_name("11-2"), "Геннадий Покемонов")
        self.assertIsNone(get_doc_owner_name("999"))

    def test_get_all_doc_owners_names(self):
        owners = get_all_doc_owners_names()
        expected = {"Василий Гупкин", "Геннадий Покемонов", "Аристарх Павлов"}
        self.assertEqual(owners, expected)

    def test_remove_doc_from_shelf(self):
        remove_doc_from_shelf("11-2")
        self.assertNotIn("11-2", app.directories['1'])

    def test_add_new_shelf(self):
        shelf, created = add_new_shelf("4")
        self.assertTrue(created)
        self.assertIn("4", app.directories)
        self.assertEqual(app.directories["4"], [])

    def test_append_doc_to_shelf(self):
        append_doc_to_shelf("new_doc", "999")
        self.assertIn("new_doc", app.directories["999"])

    def test_delete_doc(self):
        doc_number, result = delete_doc("11-2")
        self.assertTrue(result)
        self.assertNotIn({"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"}, app.documents)
        self.assertNotIn("11-2", app.directories['1'])

    def test_get_doc_shelf(self):
        shelf = get_doc_shelf("11-2")
        self.assertEqual(shelf, '1')
        self.assertIsNone(get_doc_shelf("999"))

    def test_move_doc_to_shelf(self):
        result = move_doc_to_shelf("11-2", "3")
        self.assertEqual(result, 'Документ номер "11-2" был перемещен на полку номер "3"')
        self.assertIn("11-2", app.directories['3'])
        self.assertNotIn("11-2", app.directories['1'])

    def test_show_document_info(self):
        doc = {"type": "passport", "number": "123", "name": "Иван"}
        self.assertEqual(show_document_info(doc), 'passport "123" "Иван"')

    def test_show_all_docs_info(self):
        result = show_all_docs_info()
        self.assertIn('passport "2207 876234" "Василий Гупкин"', result)

    def test_add_new_doc(self):
        result = add_new_doc("555", "driver license", "Петр Петров", "3")
        self.assertEqual(result, 'На полку "3" добавлен новый документ: 555')
        self.assertIn({"type": "driver license", "number": "555", "name": "Петр Петров"}, app.documents)
        self.assertIn("555", app.directories["3"])


if __name__ == '__main__':
    unittest.main()
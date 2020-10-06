import unittest
import os
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, MenuItem, Category
#https://chris-campos.us.auth0.com/authorize?audience=fdm&response_type=token&client_id=3dAm6kZYfeaCxH6ehGUHR3V6MMrbXlj0&redirect_uri=http://0.0.0.0:8080/menu/


class FDMTestCase(unittest.TestCase):
    """This class represents the customer accesses test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.menu_item = {
                "name": 'mac and cheese',
                "ingredients": '[{"ingredient_name": "noodle", "ingredient_amount": 10},'\
                '{"ingredient_name": "cheese", "ingredient_amount": 5}]',
                "category": 1,
                "price": 10
        }
        self.category = {
            "type": "breakfast"
        }
        self.chef_header = {'Authorization': 'Bearer {}'.format('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZDV042Tn'
                                                                'NTa21jU293ajliZVMtVCJ9.eyJpc3MiOiJodHRwczovL2NocmlzLWN'
                                                                'hbXBvcy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY3Y2Q2'
                                                                'ZGE4MTU1MWYwMDZlNDMwYmY2IiwiYXVkIjoiZmRtIiwiaWF0Ijox'
                                                                'NjAyMDE3NTcyLCJleHAiOjE2MDIwMjQ3NzIsImF6cCI6IjNkQW02a'
                                                                '1pZZmVhQ3hINmVoR1VIUjNWNk1NcmJYbGowIiwic2NvcGUiOiIiLCJ'
                                                                'wZXJtaXNzaW9ucyI6WyJkZWxldGU6bWVudV9pdGVtIiwiZ2V0OmNhd'
                                                                'GVnb3JpZXMiLCJnZXQ6bWVudV9pdGVtIiwicGF0Y2g6bWVudV9pdGV'
                                                                'tIiwicG9zdDptZW51X2l0ZW0iXX0.Sb3pKDh0jRDLveLPdl7Pop4-a'
                                                                'r3S1nlYn9OhdJE9YwGSHaqjVbGFRjOkOSmjNCFuQjUHN9KQW8mquDn'
                                                                '4bUgUyh6eILwMkQqkDFsh7Rsvs3nOp1kW2mjFTYj7inFMN28fpxiAN'
                                                                'CiyUbr0hyxNN06GV1iF_snhjUuEC7WrITHJabCyJxvZysemWjXew4H'
                                                                'B8aOcrfuZ5aEGv-yRVY44MQLm12SqtoHo12ZhciiK22HB795LGepCs'
                                                                'ecjeCO0OLUmBsHleZWg8nBYhH3SbJ3PjeTKJIsvIJZcckIKRUC2jqR'
                                                                'GDS6f74CBqCcCXthVHt3Al7rLh4xrhk8wqUIaovSGJZIkcQ')}
        self.owner_header = {'Authorization': 'Bearer {}'.format('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZDV042T'
                                                                 'nNTa21jU293ajliZVMtVCJ9.eyJpc3MiOiJodHRwczovL2NocmlzL'
                                                                 'WNhbXBvcy51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdX'
                                                                 'RoMnwxMTE4NDQ5MzUzNjc3ODE3Mjk3OTgiLCJhdWQiOlsiZmRtIiw'
                                                                 'iaHR0cHM6Ly9jaHJpcy1jYW1wb3MudXMuYXV0aDAuY29tL3VzZXJp'
                                                                 'bmZvIl0sImlhdCI6MTYwMjAxNzcwOSwiZXhwIjoxNjAyMDI0OTA5L'
                                                                 'CJhenAiOiIzZEFtNmtaWWZlYUN4SDZlaEdVSFIzVjZNTXJiWGxqMC'
                                                                 'IsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXN'
                                                                 'zaW9ucyI6WyJkZWxldGU6Y2F0ZWdvcmllcyIsImRlbGV0ZTptZW51'
                                                                 'X2l0ZW0iLCJnZXQ6Y2F0ZWdvcmllcyIsImdldDptZW51X2l0ZW0iL'
                                                                 'CJwYXRjaDptZW51X2l0ZW0iLCJwb3N0OmNhdGVnb3JpZXMiLCJwb3'
                                                                 'N0Om1lbnVfaXRlbSJdfQ.ethcB36E6f5wvTTesNH8Q3gjNru3LGpf'
                                                                 'TQ7w713XqhQafHZ_4f_TnrzghM31D1S0hWePbtSQ3i-77ASxipL_u'
                                                                 'q2bzwm7YmGrxp8W-yrZxawXQbhBJ_PcvmsQCqJmQLfTNznicQCBSh'
                                                                 'Uz16VnvJZ3ZJYwVj9WeRJetIzkdTtAPUI6_QCZvUVL2y_-kqs0PLn'
                                                                 'xkooAxKAp5ytB5uqt268JGgrOPbX2mgyvUNZa1KkhpQpAFtBkWQBb'
                                                                 'Gz5etUt7pidiD9sb4KGlngzy6AYvNBgJEJdVhdlbow_38Cui0wqJG'
                                                                 'UZ9lo4br_aXGJJEtIVlyRAchg_-3vSjxM3yx2pLxcjoRw')}
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_error_get_categories(self):
        res = self.client().get('/menu/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        # No access since there is permissions
        self.assertEqual(data['success'], False)

    def test_get_categories_wrong(self):
        res = self.client().get('/menu/category')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_menu(self):
        res = self.client().get('/menu')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(type(data['menu_items']) == list)

    def test_get_menu_wrong(self):
        res = self.client().get('/men')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_menu_with_new_value(self):
        new_menu_item = MenuItem(name=self.menu_item.get('name'), category=self.menu_item.get('category'),
                                 ingredients=self.menu_item.get('ingredients'), price=self.menu_item.get('price'))
        new_menu_item.insert()
        res = self.client().get('/menu')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['menu_items']) >= 0)

    def test_add_value_permission(self):
        res = self.client().post('/menu', json=self.menu_item)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_menu_item_bare(self):
        new_menu_item = MenuItem(name=self.menu_item.get('name'), category=self.menu_item.get('category'),
                                 ingredients=self.menu_item.get('ingredients'), price=self.menu_item.get('price'))
        new_menu_item.insert()
        menu_item_id = new_menu_item.id
        menu_item = MenuItem.query.filter(MenuItem.id == menu_item_id).one_or_none()
        self.assertIsNotNone(menu_item)
        menu_item.delete()
        menu_item_deleted = MenuItem.query.filter(MenuItem.id == menu_item_id).one_or_none()
        self.assertIsNone(menu_item_deleted)
        res = self.client().get('/menu')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_permission(self):
        res = self.client().delete('/menu/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_patch_permission(self):
        new_menu_item = MenuItem(name=self.menu_item.get('name'), category=self.menu_item.get('category'),
                                 ingredients=self.menu_item.get('ingredients'), price=self.menu_item.get('price'))
        new_menu_item.insert()
        menu_item_id = new_menu_item.id
        res = self.client().patch('/menu/{}'.format(menu_item_id, json={"price": 200}))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

# RBAC Tests

    # Chef Tests
    def test_get_menu_item(self):
        res = self.client().get('/menu/categories', headers=self.chef_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_menu_item(self):
        res = self.client().post('/menu', json=self.menu_item, headers=self.chef_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_menu_item(self):
        new_menu_item = MenuItem(name=self.menu_item.get('name'), category=self.menu_item.get('category'),
                                 ingredients=self.menu_item.get('ingredients'), price=self.menu_item.get('price'))
        new_menu_item.insert()
        menu_item_id = new_menu_item.id
        menu_item = MenuItem.query.filter(MenuItem.id == menu_item_id).one_or_none()
        self.assertIsNotNone(menu_item)
        res = self.client().patch('/menu/{}'.format(menu_item_id), json={"price": 100}, headers=self.chef_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_menu_item(self):
        new_menu_item = MenuItem(name=self.menu_item.get('name'), category=self.menu_item.get('category'),
                                 ingredients=self.menu_item.get('ingredients'), price=self.menu_item.get('price'))
        new_menu_item.insert()
        menu_item_id = new_menu_item.id
        menu_item = MenuItem.query.filter(MenuItem.id == menu_item_id).one_or_none()
        self.assertIsNotNone(menu_item)
        res = self.client().delete('/menu/{}'.format(menu_item_id), headers=self.chef_header)
        data = json.loads(res.data)
        menu_item = MenuItem.query.filter(MenuItem.id == menu_item_id).one_or_none()
        self.assertIsNone(menu_item)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Owner Tests
    def test_get_categories(self):
        res = self.client().get('/menu/categories', headers=self.owner_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_add_category(self):
        res = self.client().post('/menu/categories', json=self.category, headers=self.owner_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_view_category(self):
        new_category = Category(type='new_type')
        new_category.insert()
        category_id = new_category.id
        res = self.client().get('/menu/categories/{}'.format(category_id), json=self.category, headers=self.owner_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_category(self):
        new_category = Category(type='new_type')
        new_category.insert()
        category_id = new_category.id
        category = Category.query.filter(Category.id == category_id).one_or_none()
        self.assertIsNotNone(category)
        res = self.client().delete('/menu/categories/{}'.format(category_id), headers=self.owner_header)
        data = json.loads(res.data)
        category = Category.query.filter(Category.id == category_id).one_or_none()
        self.assertIsNone(category)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_error_add_category(self):
        res = self.client().post('/menu/categories', headers=self.owner_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_error_view_category(self):
        res = self.client().get('/menu/categories/-1', json=self.category, headers=self.owner_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_error_delete_category(self):
        res = self.client().delete('/menu/categories/1000', headers=self.owner_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)


if __name__ == "__main__":
    unittest.main()

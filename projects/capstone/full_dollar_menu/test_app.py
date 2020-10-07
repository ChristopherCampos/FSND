import unittest
import os
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, MenuItem, Category
#https://chris-campos.us.auth0.com/authorize?audience=fdm&response_type=token&client_id=3dAm6kZYfeaCxH6ehGUHR3V6MMrbXlj0&redirect_uri=https://full-dollar-menu.herokuapp.com/menu


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
        self.chef_header = {'Authorization': 'Bearer {}'.format('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZDV042TnNTa21jU293ajliZVMtVCJ9.eyJpc3MiOiJodHRwczovL2NocmlzLWNhbXBvcy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY3Y2Q2ZGE4MTU1MWYwMDZlNDMwYmY2IiwiYXVkIjoiZmRtIiwiaWF0IjoxNjAyMDI4ODM5LCJleHAiOjE2MDIwMzYwMzksImF6cCI6IjNkQW02a1pZZmVhQ3hINmVoR1VIUjNWNk1NcmJYbGowIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6bWVudV9pdGVtIiwiZ2V0OmNhdGVnb3JpZXMiLCJnZXQ6bWVudV9pdGVtIiwicGF0Y2g6bWVudV9pdGVtIiwicG9zdDptZW51X2l0ZW0iXX0.JFbQTbfjOfAlQeDDOzbSO6fZ3wbW2JPU4YMcskY0ZVjL_ntWY3kPGiBabtl8brfiIYEj3VDpAUzfAD8YtjeH1OsAUDaOl_z3H06MIo0Z0p2pxA034ifiATw06KVc15lV5FWnaoPSwkEt8s22qAy9ZWdN443-qK4ziRnJOd2jo7ZmzpXtUC9yEhd2OrLlLArNf7fESmSesLKr8Tpdsonn7rSKKDQO99fuE4HJylbb6c0KGOV3-MwR723_P00RBT7N4Gng5OdFCrMJq3Zdu4EaGgjTE8MhcddOLWJTskHeUjveCvdddP_iwLz_8ya7BA-40aC6wGTSzHLMttQIwJouxQ')}
        self.owner_header = {'Authorization': 'Bearer {}'.format('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZDV042TnNTa21jU293ajliZVMtVCJ9.eyJpc3MiOiJodHRwczovL2NocmlzLWNhbXBvcy51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTE4NDQ5MzUzNjc3ODE3Mjk3OTgiLCJhdWQiOlsiZmRtIiwiaHR0cHM6Ly9jaHJpcy1jYW1wb3MudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYwMjAyODkxOCwiZXhwIjoxNjAyMDM2MTE4LCJhenAiOiIzZEFtNmtaWWZlYUN4SDZlaEdVSFIzVjZNTXJiWGxqMCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Y2F0ZWdvcmllcyIsImRlbGV0ZTptZW51X2l0ZW0iLCJnZXQ6Y2F0ZWdvcmllcyIsImdldDptZW51X2l0ZW0iLCJwYXRjaDptZW51X2l0ZW0iLCJwb3N0OmNhdGVnb3JpZXMiLCJwb3N0Om1lbnVfaXRlbSJdfQ.gKSYMzVGkNoV61_QkuVEqfK_MC1TvAjFCMJMiq-TAKnvOPJXtOYtYrkVYByAzDjh05ic4D_FiVjUKT1Ov2MoPxDmjJ3boZzAWbj_PFvaCU2h9_Kixe9WE6tZRGZFKuXOAR1HO-tqJ8aZvdzHIaXD2S2mDD4ldf8u7CHDraI-crFfdcrumnmbFzt9hmvpApWGZyMAO8yKW_tTplHAH4ni65Lc_2MIfMC9gl-lISZuCNAPRQnR_XsLQhANTBtaUf64BOXTBcy1J1WWJbQmggTzQNAUPgvPJQkiC_Aw5POHIS1yrbJBtUFaEw9u9bp0doEub7C2P7Y_kg7bYPxQQ3ckgQ')}
        #if os.environ['CHEF_TOKEN']:
        #    self.chef_header = {'Authorization': "Bearer {}".format(os.environ['CHEF_TOKEN'])}
        #if os.environ['OWNER_TOKEN']:
        #    self.owner_header = {'Authorization': "Bearer {}".format(os.environ['OWNER_TOKEN'])}
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

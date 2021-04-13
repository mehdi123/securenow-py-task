from mysql.connector import connect, Error

DB_HOST = 'localhost'
DB_USER = 'root'
DB_password = 'root'

class DB:
    def __init__(self):
        try:
            connection = connect(
                        host=DB_HOST,
                        user=DB_USER,
                        password=DB_PASSWORD)
            self.cursor = connection.cursor()
        except Exception as e:
            print(e)
    
    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

class Schema:

    def __init__(self):
        self.customer_schema = {"name": "", "email": "", "phone": "", "address": ""}
    
    def check_customer(self, target: dict):
        if not (isinstance(self.customer_schema, dict) and isinstance(target, dict)):
            if type(self.customer_schema) == type([]) and type(target) == type([]):
                if len(self.customer_schema) == len(target):
                    for i in range(len(self.customer_schema)):
                        if not self.check_customer(target[i]):
                            return False
                    return True
                else:
                    return False
            else:
                return type(self.customer_schema) == type(target)
        else:
            if not self.customer_schema.keys() == target.keys():
                return False

            for sk in self.customer_schema:
                if not self.check_customer(target[sk]):
                    return False
            return True

class Querier:
    def __init__(self):
        self.db = DB()
        self.schema = Schema()
    
    def get_customer(self, _id):
        data = self.db.execute_query(f'SELECT * FROM CUSTOMER WHERE id = {_id}')
        if data:
            return {"id": data[0],
                    "name": data[1],
                    "email": data[2],
                    "phone": data[3],
                    "address": data[4]}
        return {}
    
    def create_customer(self, **kwargs):
        if self.schema.check_customer(kwargs):  # checks the customer info schema
            result = self.db.execute_query(f'INSERT INTO Customer VALUES(\
                                                {kwargs.get('name')},\
                                                {kwargs('email')},\
                                                {kwargs.get('phone')},\
                                                {kwargs.get('address')})')
            if result:
                return True
        return False

    def update_customer(self, **kwargs):
        _id = kwargs.get('id')
        if _id:
            set_statement = ','.join(column+'='+kwargs[column] for column in kwargs if column != 'id')
            result = self.db.execute_query(f'UPDATE TABLE CUSTOMER SET {set_statement} WHERE id = {_id}')
            if result:
                return True
        return False
    
    def delete_customer(self, **kwargs):
        _id = kwargs.get('id')
        if _id:
            result = self.db.execute_query(f'DELETE FROM CUSTOMER WHERE id={_id}')
            if result:
                return True
        return False
    
    def get_customer(self, _id):
        if _id:
            result = self.db.execute_query(f'SELECT * FROM CUSTOMER WHERE id={_id}')
            if result:
                return {"id": _id,
                        "name": result[1],
                        "email": result[2],
                        "phone": result[3],
                        "address": result[4]}
        return {}
        
querier = Querier()
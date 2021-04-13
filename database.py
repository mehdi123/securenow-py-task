from pymysql import connect

DB_HOST = 'db'
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_PORT = 3306
DB_NAME='main'

class DB:
    def __init__(self):
        try:
            self.connection = connect(
                        host=DB_HOST,
                        port=DB_PORT,
                        user=DB_USER,
                        database=DB_NAME,
                        password=DB_PASSWORD)
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(e)
    
    def execute_query(self, query, commit=True):
        try:
            self.cursor.execute(query)
            if commit:
                self.connection.commit()
        except Exception as e:
            print(e)
    
    def rows_affected(self):
        return self.cursor.rowcount
    
    def get_query_result(self):
        return self.cursor.fetchall()

class Schema:
    """
        Checking the validity of the scehma
    """

    def __init__(self):
        self.customer_schema = {"name": "", "email": "", "phone": "", "address": ""}

    def validate(self, target):
        return self._check(self.customer_schema, target)

    def _check(self, source: dict, target: dict):
        if not (isinstance(source, dict) and isinstance(target, dict)):
            if type(source) == type("") and type(target) == type(""):
                return type(source) == type(target)
        else:
            if not source.keys() == target.keys():
                return False

            for sk in source:
                if not self._check(source[sk], target[sk]):
                    return False
            return True

class CustomerQuerier:

    def __init__(self):

        self.db = DB()
        self.schema = Schema()
    
    def get_customer(self, _id):

        data = self.db.execute_query(f'SELECT * FROM Customer WHERE id = {_id}')
        if data:
            return {"id": data[0],
                    "name": data[1],
                    "email": data[2],
                    "phone": data[3],
                    "address": data[4]}
        return {}
    
    def create_customer(self, **kwargs):

        if self.schema.validate(kwargs):  # checks the customer info schema
            query = f"INSERT INTO Customer (name, email, phone, address) VALUES(\"{kwargs.get('name')}\", \"{kwargs.get('email')}\", \"{kwargs.get('phone')}\", \"{kwargs.get('address')}\")"
            self.db.execute_query(query)
            if self.db.rows_affected() > 0:
                return self._find_customer(kwargs)
        return False
    
    def _find_customer(self, kwargs):
        " This function is used after creating customer "

        where_clause = ' AND '.join(f'{key}="{kwargs[key]}"' for key in kwargs)
        query = f"SELECT * FROM Customer WHERE {where_clause}"
        self.db.execute_query(query, commit=False)
        result = self.db.get_query_result()
        if len(result) > 0:
            return result[0]
        return None

    def update_customer(self, **kwargs):

        _id = kwargs.get('id')
        if _id:
            set_statement = ','.join(f"{column}='{kwargs[column]}'" for column in kwargs if column != 'id')
            self.db.execute_query(f'UPDATE Customer SET {set_statement} WHERE id = {_id}')
            if self.db.rows_affected():
                return True
        return False
    
    def delete_customer(self, **kwargs):

        _id = kwargs.get('id')
        if _id:
            self.db.execute_query(f'DELETE FROM Customer WHERE id={_id}')
            if self.db.rows_affected():
                return True
        return False
    
    def get_customer(self, _id):

        if _id:
            self.db.execute_query(f'SELECT * FROM Customer WHERE id={_id}', commit=False)
            result = self.db.get_query_result()
            if result:
                return {"id": _id,
                        "name": result[0][1],
                        "email": result[0][2],
                        "phone": result[0][3],
                        "address": result[0][4]}
        return {}

querier = CustomerQuerier()
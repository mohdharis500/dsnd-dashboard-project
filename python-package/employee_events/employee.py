# Import the QueryBase class
from query_base import QueryBase

# Import dependencies needed for SQL execution
from sql_execution import QueryMixin  

# Define a subclass of QueryBase called Employee
class Employee(QueryBase):
    # Set the class attribute `name` to the string "employee"
    name = "employee"

    # Define a method called `names`
    # that returns a list of tuples from SQL execution
    def names(self):
        # Query 3: select employee full name and id for all employees
        query = f"""
            SELECT full_name, employee_id
            FROM {self.name}
        """
        # Execute the query and return results
        return execute(query)

    # Define a method called `username` that receives an `id` argument
    # Returns the full name of the employee with that id
    def username(self, id):
        # Query 4: select employee full name for a specific id
        query = f"""
            SELECT full_name
            FROM {self.name}
            WHERE employee_id = {id}
        """
        return execute(query)

    # Method to return model data as a pandas DataFrame
    def model_data(self, id):
        import pandas as pd

        query = f"""
            SELECT SUM(positive_events) positive_events
                 , SUM(negative_events) negative_events
            FROM {self.name}
            JOIN employee_events
                USING({self.name}_id)
            WHERE {self.name}.{self.name}_id = {id}
        """
        # Execute the query
        results = execute(query)
        # Convert results to a pandas DataFrame and return
        df = pd.DataFrame(results, columns=['positive_events', 'negative_events'])
        return df

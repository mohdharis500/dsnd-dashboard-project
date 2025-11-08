# Import the QueryBase class
from query_base import QueryBase

# Import dependencies for SQL execution
from sql_execution import QueryMixin  
import pandas as pd

# Create a subclass of QueryBase called `Team`
class Team(QueryBase):
    # Set the class attribute `name` to "team"
    name = "team"

    # Define a `names` method that returns a list of tuples
    def names(self):
        # Query 5: select team_name and team_id for all teams
        query = f"""
            SELECT team_name, team_id
            FROM {self.name}
        """
        return execute(query)

    # Define a `username` method that receives an ID argument
    # Returns a list of tuples with the team name
    def username(self, id):
        # Query 6: select team_name for a specific ID
        query = f"""
            SELECT team_name
            FROM {self.name}
            WHERE team_id = {id}
        """
        return execute(query)

    # Method to return model data as a pandas DataFrame
    def model_data(self, id):
        query = f"""
            SELECT positive_events, negative_events FROM (
                    SELECT employee_id,
                           SUM(positive_events) positive_events,
                           SUM(negative_events) negative_events
                    FROM {self.name}
                    JOIN employee_events
                        USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                    GROUP BY employee_id
                   )
        """
        results = execute(query)
        df = pd.DataFrame(results, columns=['positive_events', 'negative_events'])
        return df

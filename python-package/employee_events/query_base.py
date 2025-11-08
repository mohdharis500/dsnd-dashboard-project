# Import any dependencies needed to execute SQL queries
import pandas as pd
from sql_execution import QueryMixin    # assuming `execute` returns list of tuples

# Define a class called QueryBase
class QueryBase:
    # Create a class attribute called `name`
    # set the attribute to an empty string
    name = ""

    # Define a `names` method that receives no arguments
    def names(self):
        # By default, return empty list; subclasses can override
        return []

    # Define an `event_counts` method that receives an `id` argument
    # This method should return a pandas dataframe
    def event_counts(self, id):
        # QUERY 1: group by event_date and sum positive/negative events
        query = f"""
            SELECT event_date,
                   SUM(positive_events) AS positive_events,
                   SUM(negative_events) AS negative_events
            FROM {self.name}
            JOIN employee_events
                USING({self.name}_id)
            WHERE {self.name}.{self.name}_id = {id}
            GROUP BY event_date
            ORDER BY event_date
        """
        results = execute(query)
        df = pd.DataFrame(results, columns=['event_date', 'positive_events', 'negative_events'])
        return df

    # Define a `notes` method that receives an `id` argument
    # This method should return a pandas dataframe
    def notes(self, id):
        # QUERY 2: return notes for this table
        query = f"""
            SELECT note_date, note
            FROM notes
            JOIN {self.name}
                USING({self.name}_id)
            WHERE {self.name}.{self.name}_id = {id}
            ORDER BY note_date
        """
        results = execute(query)
        df = pd.DataFrame(results, columns=['note_date', 'note'])
        return df

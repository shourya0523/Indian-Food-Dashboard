import pandas as pd
import cleaner as cl

class FOODAPI:
    def load_food(self, filename='indian_food.csv'):
        """
        Load and clean the food dataset from CSV file.

        Args:
            filename : str
                Path to the CSV file containing food data
        """
        self.food = cl.clean_df(pd.read_csv(filename))

    def get_frame(self, columns=None):
        """
        Return the complete or filtered food dataframe.

        Args:
            columns : list, optional
                List of column names to return
        Returns:
            pandas.DataFrame
                Complete or filtered food dataframe
        """
        if columns:
            return self.food[columns]
        else:
            return self.food
    
    def get_foods(self):
        """
        Return a list of all available food names.

        Returns:
            list
                List of all food names in the dataset
        """
        return self.food['name'].tolist()

    def get_food_ingredients(self, food_names):
        """
        Get ingredients for specific foods.

        Args:
            food_names : list
                List of food names to get ingredients for
        Returns:
            dict
                Dictionary mapping food names to their ingredients
        """
        food_ing_df = self.food[self.food['name'].isin(food_names)]
        food_ing_dict = food_ing_df.set_index('name')['ingredients'].to_dict()
        return food_ing_dict
    
    def get_available_filters(self):
        """
        Get list of categorical columns that can be used for filtering.

        Returns:
            list
                List of column names excluding 'name', 'ingredients', prep_time, and cook_time
        """
        excluded_cols = ['name', 'ingredients','prep_time','cook_time']
        return [col for col in self.food.columns if col not in excluded_cols]
    
    def get_flows(self, source_col='ingredient', target_col='category', min_count=0):
        """
        Create a dataframe showing flows between source and target columns.
        
        Args:
            source_col : str
                The source column name
            target_col : str
                The target column name
            min_count : int
                Minimum count threshold for including flows
            
        Returns:
            pandas.DataFrame
                Dataframe with columns [source, target, count]
        """
        flows = []
        for _, row in self.food.iterrows():
            flows.append({
                'source': row[source_col],
                'target': row[target_col],
                'count': 1
            })
        
        flow_df = pd.DataFrame(flows)
        flow_df = flow_df.groupby(['source', 'target']).sum().reset_index()
        
        if min_count > 0:
            flow_df = flow_df[flow_df['count'] >= min_count]
        
        return flow_df



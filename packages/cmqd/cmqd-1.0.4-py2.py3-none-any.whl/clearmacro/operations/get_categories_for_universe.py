import pandas as pd


class GetCategoriesForUniverse:
    def get_categories_for_universe(self, universe: str):
        """
        Function to retrieve the list of categories corresponding to the passed universe.

        Args:
            universe (str): One of the signal universes. Available options are the "name" fields from the list of universe objects obtained by calling the get_signal_universes method.

        Returns:
            JSON list of category objects.
        """
        try:
            universes_df = self.json_to_df(self.get_signal_universes())
            universe_id = universes_df[universes_df.name == universe].universeId.iloc[0]
            return self.get_categories_for_universe_id(universe_id)
        except IndexError:
            raise ValueError(self._inputErrorMessage)

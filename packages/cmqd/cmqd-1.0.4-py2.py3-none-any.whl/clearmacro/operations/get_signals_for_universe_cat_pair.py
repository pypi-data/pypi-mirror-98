import pandas as pd


class GetSignalsForUniverseCatPair:
    def get_signals_for_universe_cat_pair(self, universe: str, category: str):
        """
        Function to retrieve all signals belonging to the given universe, category pair.

        Args:
            universe (str): One of the signal universes. Available options are the "name" fields from the list of universe objects obtained by calling the get_signal_universes method.
            category (str): One of the categories of the above universe. Available options are the "name" fields from the list of category objects obtained by calling get_categories_for_universe(universe).

        Returns:
            JSON list of signal objects.
        """
        try:
            universes_df = self.json_to_df(self.get_signal_universes())
            universe_id = universes_df[universes_df.name == universe].universeId.iloc[0]
            categories_df = self.json_to_df(
                self.get_categories_for_universe_id(universe_id)
            )
            category_id = categories_df[categories_df.name == category].categoryId.iloc[0]
            return self.get_signals_for_universe_cat_pair_id(universe_id, category_id)
        except IndexError:
            raise ValueError(self._inputErrorMessage)

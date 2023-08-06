class GetSignalsForUniverseCatPairId:
    def get_signals_for_universe_cat_pair_id(self, universe_id: int, category_id: int):
        """
        Function to retrieve all signals belonging to the given universe, category pair by id.

        Args:
            universe_id (int): One of the signal universes. Available options are the "universeId" fields from the list of universe objects obtained by calling the get_signal_universes method.
            category_id (int): One of the categories of the above universe. Available options are the "categoryId" fields from the list of category objects obtained by calling get_categories_for_universe_id(universe_id).

        Returns:
            JSON list of signal objects.
        """
        request_params = {
            "method": "get",
            "path": f"/api/signals/universes/{universe_id}/categories/{category_id}",
        }

        response = self._request(**request_params)

        return response

class GetCategoriesForUniverseId:
    def get_categories_for_universe_id(self, universe_id: int):
        """
        Function to retrieve the list of categories corresponding to the passed universe id.

        Args:
            universe_id (int): One of the signal universes. Available options are the "universeId" fields from the list of universe objects obtained by calling the get_signal_universes method.

        Returns:
            JSON list of category objects.
        """
        request_params = {
            "method": "get",
            "path": f"/api/signals/universes/{universe_id}/categories",
        }

        response = self._request(**request_params)

        return response

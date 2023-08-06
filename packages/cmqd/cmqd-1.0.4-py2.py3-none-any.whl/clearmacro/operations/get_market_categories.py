class GetMarketCategories:
    def get_market_categories(self):
        """
        Function to retrieve the list of all market categories.

        Returns:
            JSON list of market category objects.
        """
        request_params = {
            "method": "get",
            "path": "/api/signals/markets/marketcategories",
        }

        response = self._request(**request_params)

        return response

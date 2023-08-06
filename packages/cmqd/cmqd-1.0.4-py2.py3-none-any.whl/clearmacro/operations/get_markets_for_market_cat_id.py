class GetMarketsForMarketCatId:
    def get_markets_for_market_cat_id(self, market_category_id: int):
        """
        Function to retrieve the list of markets corresponding to the passed market category id.

        Args:
            market_category_id (int): One of the market categories. Available options are the "marketCategoryId" fields from the list of market category objects obtained by calling the get_market_categories method.

        Returns:
            JSON list of market objects.
        """
        request_params = {
            "method": "get",
            "path": f"/api/signals/markets/marketcategories/{market_category_id}",
        }

        response = self._request(**request_params)

        return response

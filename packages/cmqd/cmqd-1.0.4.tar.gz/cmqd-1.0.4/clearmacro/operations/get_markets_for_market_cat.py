class GetMarketsForMarketCat:
    def get_markets_for_market_cat(self, market_category: str):
        """
        Function to retrieve the list of markets corresponding to the passed market category.

        Args:
            market_category (str): One of the market categories. Available options are the "name" fields from the list of market category objects obtained by calling the get_market_categories method.

        Returns:
            JSON list of market objects.
        """
        try:
            market_categories_df = self.json_to_df(self.get_market_categories())
            market_category_id = market_categories_df[
                market_categories_df.name == market_category
            ].marketCategoryId.iloc[0]
            return self.get_markets_for_market_cat_id(market_category_id)
        except IndexError:
            raise ValueError(self._inputErrorMessage)

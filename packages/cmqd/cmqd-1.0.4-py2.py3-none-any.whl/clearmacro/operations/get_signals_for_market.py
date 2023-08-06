class GetSignalsForMarket:
    def get_signals_for_market(self, market: str):
        """
        Function to retrieve the list of signals available for the given market.

        Args:
            market (str): One of the valid markets. Available options are the "name" fields from the list of market objects obtained by calling the get_all_markets method.

        Returns:
            JSON list of signal objects.
        """
        try:
            markets_df = self.json_to_df(self.get_all_markets())
            market_id = markets_df[markets_df.name == market].classId.iloc[0]
            return self.get_signals_for_market_id(market_id)
        except IndexError:
            raise ValueError(self._inputErrorMessage)

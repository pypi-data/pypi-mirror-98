class GetResearchTypesForSignalMarketPair:
    def get_research_types_for_signal_market_pair(self, signal: str, market: str):
        """
        Function to retrieve the list of research types corresponding to the passed signal and market.

        Args:
            signal (str): One of the signals. Available options are the "name" fields from the list of signal objects obtained by calling the get_signals_catalogue method.
            market (str): One of the valid markets for the above signal. Available options are the "name" fields from the list of market objects obtained by calling the get_markets_for_signal(signal) method.

        Returns:
            JSON list of research type objects.
        """
        try:
            signals_df = self.json_to_df(self.get_signals_catalogue())
            signal_id = signals_df[signals_df.name == signal].signalId.iloc[0]
            markets_df = self.json_to_df(self.get_all_markets())
            market_id = markets_df[markets_df.name == market].classId.iloc[0]
            return self.get_research_types_for_signal_market_pair_id(signal_id, market_id)
        except IndexError:
            raise ValueError(self._inputErrorMessage)

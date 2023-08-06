class GetMarketsForSignal:
    def get_markets_for_signal(self, signal: str):
        """
        Function to retrieve the list of markets corresponding to the passed signal.

        Args:
            signal (str): One of the signals. Available options are the "name" fields from the list of signals objects obtained by calling the get_signals_catalogue method.

        Returns:
            JSON list of market objects.
        """
        try:
            signals_df = self.json_to_df(self.get_signals_catalogue())
            signal_id = signals_df[signals_df.name == signal].signalId.iloc[0]
            return self.get_markets_for_signal_id(signal_id)
        except IndexError:
            raise ValueError(self._inputErrorMessage)

class GetSignalSeries:
    def get_signal_series(
        self,
        signal: str,
        market: str,
        research_type: str,
        last_date_only=False,
        start_date=None,
        end_date=None,
        frequency_key=None,
    ):
        """
        Function to retrieve a signal time series.

        Args:
            signal (str): Options are "name" fields from list of signal objects returned by get_signals_catalogue.
            market (str): Options are "name" fields from list of market objects returned by get_markets_for_signal(signal).
            research_type (str): Options are "name" fields from list of research type objects returned by get_research_types_for_signal_market_pair(signal, market).
            last_date_only (bool, optional): Flag indicating if only the last date of the time series is desired.
            start_date (str, optional): Start date of the series in ISO format YYYY-MM-DD.
            end_date (str, optional): End date of the series in ISO format YYYY-MM-DD.
            frequency_key (str): One of the desired frequencies (None is for all values available, undetermined frequency):

            D, (Daily - all days)
            WD, (Weekdays)
            W_MON, (Weekly data on Mondays)
            W_TUE, (Weekly data on Tuesdays)
            W_WED, (Weekly data on Wednesdays)
            W_THU, (Weekly data on Thursdays)
            W_FRI, (Weekly data on Fridays)
            W_SAT, (Weekly data on Saturdays)
            W_SUN, (Weekly data on Sundays)
            M, (Monthly data - end of month)
            MS, (Monthly data - start of month)
            Q, (Quarterly data - end of quarter)
            QS (Quarterly data - start of quarter)

        Examples:
            >>> client.get_signal_series('Crossborder Flow', 'US', 'Back-test Level', last_date_only=False, start_date='2016-1-1', end_date='2020-10-16')

        Returns:
            Time series object.
        """
        try:
            signals_df = self.json_to_df(self.get_signals_catalogue())
            signal_id = signals_df[signals_df.name == signal].signalId.iloc[0]
            markets_df = self.json_to_df(self.get_all_markets())
            market_id = markets_df[markets_df.name == market].classId.iloc[0]
            research_types_df = self.json_to_df(
                self.get_research_types_for_signal_market_pair_id(signal_id, market_id)
            )
            research_type_id = research_types_df[
                research_types_df.name == research_type
            ].researchTypeId.iloc[0]
            return self.get_signal_series_id(
                signal_id,
                market_id,
                research_type_id,
                last_date_only,
                start_date,
                end_date,
                frequency_key,
            )
        except IndexError:
            raise ValueError(self._inputErrorMessage)

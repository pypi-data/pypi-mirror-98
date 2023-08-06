class GetSignalSeriesId:
    def get_signal_series_id(
        self,
        signal_id: int,
        market_id: int,
        research_type_id: int,
        last_date_only=False,
        start_date=None,
        end_date=None,
        frequency_key=None
    ):
        """
        Function to retrieve a signal time series by ids.

        Args:
            signal_id (int): Options are "signalId" fields from list of signal objects returned by get_signals_catalogue.
            market_id (int): Options are "classId" fields from list of market objects returned by get_markets_for_signal_id(signal_id).
            research_type_id (int): Options are "researchTypeId" fields from list of research type objects returned by get_research_types_for_signal_market_pair_id(signal_id, market_id).
            last_date_only (bool): Flag indicating if only the last date of the time series is desired.
            start_date (str): Start date of the series in ISO format YYYY-MM-DD.
            end_date (str): End date of the series in ISO format YYYY-MM-DD.
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
            >>> client.get_signal_series_id(8, 137, 94, last_date_only=False, start_date='2016-1-1', end_date='2020-10-16')

        Returns:
            Time series object.
        """
        uri = f"/api/signals/{signal_id}/markets/{market_id}/researchtypes/{research_type_id}"
        query_params = []

        if last_date_only:
            query_params.append(f"lastDateOnly={str(last_date_only).lower()}")
        if start_date is not None:
            query_params.append(f"&startDate={start_date}")
        if end_date is not None:
            query_params.append(f"&endDate={end_date}")
        if frequency_key is not None:
            query_params.append(f"frequencyKey={frequency_key}")

        query = "?" + "&".join(query_params)

        request_params = {
            'method': 'get',
            'path': uri + query
        }
        response = self._request(**request_params)

        return response

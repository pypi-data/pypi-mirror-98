import pandas as pd


class JsonToDf:
    def json_to_df(self, json):
        """
        Function to convert JSON/JSON list to a pandas.DataFrame object.

        Args:
            json: The JSON to be converted - this is the format all methods return.

        Returns:
            The data contained in the JSON cast as a DataFrame.
            If the data is a time series, the dataframe will be indexed by datetimes and there
            will be a 'values' column containing the value corresponding to each DateTimeIndex.
        """
        df = pd.DataFrame(json)
        if 'dateTimes' in df.columns:
            df['dateTimes'] = pd.to_datetime(df['dateTimes'])
            df = df.set_index('dateTimes')
        return df

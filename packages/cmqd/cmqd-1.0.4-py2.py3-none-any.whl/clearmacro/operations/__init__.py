from clearmacro.operations.login import Login
from clearmacro.operations.get_all_markets import GetAllMarkets
from clearmacro.operations.get_categories_for_universe import GetCategoriesForUniverse

from clearmacro.operations.get_categories_for_universe_id import (
    GetCategoriesForUniverseId,
)
from clearmacro.operations.get_market_categories import GetMarketCategories
from clearmacro.operations.get_markets_for_market_cat import GetMarketsForMarketCat
from clearmacro.operations.get_markets_for_market_cat_id import GetMarketsForMarketCatId
from clearmacro.operations.get_markets_for_signal import GetMarketsForSignal
from clearmacro.operations.get_markets_for_signal_id import GetMarketsForSignalId
from clearmacro.operations.get_research_types_for_signal_market_pair import (
    GetResearchTypesForSignalMarketPair,
)
from clearmacro.operations.get_research_types_for_signal_market_pair_id import (
    GetResearchTypesForSignalMarketPairId,
)
from clearmacro.operations.get_signal_series import GetSignalSeries
from clearmacro.operations.get_signal_series_id import GetSignalSeriesId
from clearmacro.operations.get_signal_universes import GetSignalUniverses
from clearmacro.operations.get_signals_catalogue import GetSignalsCatalogue
from clearmacro.operations.get_signals_for_market import GetSignalsForMarket
from clearmacro.operations.get_signals_for_market_id import GetSignalsForMarketId
from clearmacro.operations.get_signals_for_universe_cat_pair import (
    GetSignalsForUniverseCatPair,
)
from clearmacro.operations.get_signals_for_universe_cat_pair_id import (
    GetSignalsForUniverseCatPairId,
)
from clearmacro.operations.json_to_df import JsonToDf


class Operations(
    Login,
    GetAllMarkets,
    GetCategoriesForUniverse,
    GetCategoriesForUniverseId,
    GetMarketCategories,
    GetMarketsForMarketCat,
    GetMarketsForMarketCatId,
    GetMarketsForSignal,
    GetMarketsForSignalId,
    GetResearchTypesForSignalMarketPair,
    GetResearchTypesForSignalMarketPairId,
    GetSignalSeries,
    GetSignalSeriesId,
    GetSignalUniverses,
    GetSignalsCatalogue,
    GetSignalsForMarket,
    GetSignalsForMarketId,
    GetSignalsForUniverseCatPair,
    GetSignalsForUniverseCatPairId,
    JsonToDf,
    object,
):
    pass

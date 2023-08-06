"""Rebalance strategies."""
import datetime

import numpy as np
import numpy.typing as npt


class Rebalancer(object):
    """Interface class of Rebalance stragegy class."""

    def __init__(self) -> None:
        pass

    def apply(
        self, index: datetime.datetime, assets: npt.ArrayLike, cash: np.float64
    ) -> np.ndarray:
        """
        Apply rebalance strategy to current situation.

        Parameters
        ----------
        index
            Current date for applying rebalance.

        assets
            Current assets for applying rebalance.

        cash
            Current cash for applying rebalance.

        Returns
        -------
        Deal
        """
        pass

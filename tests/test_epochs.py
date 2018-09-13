import pytest
import numpy as np

from .context import fitgrid
from fitgrid import fake_data, epochs, errors


def test_epochs_unequal_snapshots():

    epochs_table = fake_data._generate(
        n_epochs=10, n_samples=100, n_categories=2, n_channels=32
    )

    epochs_table.drop(epochs_table.index[42], inplace=True)
    with pytest.raises(errors.FitGridError) as error:
        epochs.Epochs(epochs_table)
    assert 'differs from previous snapshot' in str(error.value)


def test__raises_error_on_epoch_index_mismatch():
    """Bad: all epochs have the same shape, but indices differ."""

    from fitgrid import TIME

    # strategy: generate epochs, but insert meaningless time index
    epochs_table = fake_data._generate(
        n_epochs=10, n_samples=100, n_categories=2, n_channels=32
    )

    # blow up index to misalign epochs and time
    bad_index = np.arange(len(epochs_table))
    epochs_table.index.set_levels(levels=bad_index, level=TIME, inplace=True)
    epochs_table.index.set_labels(labels=bad_index, level=TIME, inplace=True)

    # now time index is equal to row number in the table overall
    with pytest.raises(errors.FitGridError) as error:
        epochs.Epochs(epochs_table)

    assert 'differs from previous snapshot' in str(error.value)
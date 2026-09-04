import numpy as np
import pandas as pd
import pytest

from generate_spotify import GENRES, generate_tracks


EXPECTED_COLUMNS = {
    "track_id", "track_name", "artist", "genre", "popularity",
    "danceability", "energy", "loudness", "speechiness", "acousticness",
    "instrumentalness", "valence", "tempo", "duration_ms",
}

FEATURE_COLUMNS_0_1 = ["danceability", "energy", "acousticness", "valence"]


@pytest.fixture()
def small_df() -> pd.DataFrame:
    return generate_tracks(n=300, seed=7)


def test_has_expected_columns(small_df):
    assert EXPECTED_COLUMNS.issubset(small_df.columns)


def test_row_count_includes_injected_duplicates(small_df):
    # generate_tracks(n=300, ...) appends 20 duplicate rows on top of n.
    assert len(small_df) == 320


def test_genres_are_from_the_known_set(small_df):
    seen = set(small_df["genre"].dropna().unique())
    assert seen.issubset(set(GENRES))


def test_bounded_features_stay_in_0_1_range(small_df):
    for col in FEATURE_COLUMNS_0_1:
        values = small_df[col].dropna()
        assert values.between(0.0, 1.0).all(), f"{col} has values outside [0, 1]"


def test_messiness_is_injected(small_df):
    # Nulls, impossible tempo/duration, and duplicate rows are all
    # deliberately injected — the dataset should show every kind.
    assert small_df.isnull().any().any()
    assert (small_df["tempo"] == 0.0).any()
    assert (small_df["duration_ms"] == -1).any()
    assert small_df.duplicated().any()


def test_generation_is_deterministic_for_a_given_seed():
    first = generate_tracks(n=100, seed=42)
    second = generate_tracks(n=100, seed=42)
    pd.testing.assert_frame_equal(first, second)


def test_different_seeds_produce_different_data():
    first = generate_tracks(n=100, seed=1)
    second = generate_tracks(n=100, seed=2)
    assert not first["popularity"].equals(second["popularity"])

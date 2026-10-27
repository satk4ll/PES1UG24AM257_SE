
"""Music catalog demonstrating SQLite operations and playlist handling."""

import json
import secrets
import sqlite3

DB_CONNECTION = sqlite3.connect(":memory:")

DB_CONNECTION.execute(
    """
    CREATE TABLE songs (
        id INTEGER PRIMARY KEY,
        title TEXT,
        artist TEXT,
        plays INTEGER
    )
    """
)


def add_song(title, artist, plays=0, playlist=None):
    """Add a song to the database and playlist."""
    if playlist is None:
        playlist = []

    DB_CONNECTION.execute(
        "INSERT INTO songs (title, artist, plays) VALUES (?, ?, ?)",
        (title, artist, plays),
    )
    playlist.append(title)
    return playlist


def shuffle_pick():
    """Return a random song ID, or None if the catalog is empty."""
    song_ids = [
        row[0]
        for row in DB_CONNECTION.execute("SELECT id FROM songs")
    ]

    if not song_ids:
        return None

    return secrets.choice(song_ids)


def popularity(title):
    """Classify a song as popular, niche, or unknown."""
    row = DB_CONNECTION.execute(
        "SELECT plays FROM songs WHERE title = ?",
        (title,),
    ).fetchone()

    if row is None:
        return "unknown"

    return "popular" if row[0] > 100 else "niche"


def save_playlist(playlist):
    """Serialize a playlist to JSON."""
    return json.dumps(playlist)


def load_playlist(data):
    """Load a playlist from JSON."""
    playlist = json.loads(data)

    if not isinstance(playlist, list):
        raise ValueError("Playlist data must contain a list.")

    if not all(isinstance(song, str) for song in playlist):
        raise ValueError("Every playlist entry must be a string.")

    return playlist


def total_plays():
    """Return the total number of plays across all songs."""
    try:
        result = DB_CONNECTION.execute(
            "SELECT SUM(plays) FROM songs"
        ).fetchone()
    except sqlite3.Error:
        return 0

    return result[0] if result[0] is not None else 0


def main():
    """Run a demonstration of the music catalog."""
    playlist = add_song("Aurora", "Nila", 250)
    add_song("Monsoon", "Kavya", 40, playlist)

    serialized_playlist = save_playlist(playlist)
    loaded_playlist = load_playlist(serialized_playlist)

    if len(loaded_playlist) > 1:
        print("Multi-song playlist")

    print(
        popularity("Aurora"),
        popularity("Monsoon"),
        shuffle_pick(),
        total_plays(),
    )


if __name__ == "__main__":
    main()

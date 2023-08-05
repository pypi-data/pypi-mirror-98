"""CLI for figuring out the url for viewing results."""

from aidkit.data_access.authentication import get_url

if __name__ == "__main__":
    print(get_url())

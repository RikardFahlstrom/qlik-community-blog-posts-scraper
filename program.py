from rich import print

from qlikview_community import main as community_main
from qlikview_cookbook import main as cookbook_main


def main():
    community_main()
    cookbook_main()
    print("Done")

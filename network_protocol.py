import requests


def broadcast(miners, json_block, endpoint):
    for miner in miners:
        response = requests.post(
            miner+endpoint,
            data={'block': json_block}
        )


if __name__ == "__main__":
    pass

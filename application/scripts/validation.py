import requests


def authorization():
    url = "https://util.devi.tools/api/v2/authorize"

    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        data = response.json()

        auth = data.get("data", {}).get("authorization")
        if auth == "False":
            return False

        return True

    except requests.exceptions.RequestException as e:
        print(f"[Request Error] {e}")
    except ValueError:
        print("[Parsing Error] Response was not valid JSON.")
    except KeyError as e:
        print(f"[Key Error] Missing key: {e}")
    return False


if __name__ == "__main__":
    result = authorization()
    if result:
        print(result)

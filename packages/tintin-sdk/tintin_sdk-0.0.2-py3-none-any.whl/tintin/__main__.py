from configparser import ConfigParser
from importlib.resources import open_text

def main():
    cfg = ConfigParser()
    cfg.read_string(open_text("tintin", "config.txt").readlines())
    url = cfg.get("endpoint", "api_url")

    print('url:{}'.format(url))

if __name__ == "__main__":
    main()

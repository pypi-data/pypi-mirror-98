"""wordpress_oauth - Python REST API wrapper for WP-API/OAuth1"""
import logging
import os
from pathlib import Path

import fire
import kanilog
import requests
import yaml
from requests_oauthlib import OAuth1, OAuth1Session
from urlpath import URL

__version__ = "0.1.2"
__author__ = "fx-kirin <fx.kirin@gmail.com>"
__all__: list = []


class Wordpress:
    def __init__(self, config_file_path):
        self.log = logging.getLogger(self.__class__.__name__)
        if isinstance(config_file_path, str):
            config_file_path = Path(config_file_path)
        self.config_file_path = config_file_path.expanduser()
        self._make_auth()

    def _make_auth(self):
        config_path = self.config_file_path.parent.expanduser()
        if not config_path.exists():
            self.log.info("Creating directory %s", config_path)
            config_path.mkdir(parents=True)
        config_file = self.config_file_path
        if not config_file.exists():
            self.log.info("Creating config file %s", config_path)
            url = input("Enter your website url: ")
            key = input("Enter your OAuth Client Key: ")
            secret = input("Enter OAuth Client Secret: ")
            user_info = {"url": url, "key": key, "secret": secret}
            config_file.write_text(yaml.dump(user_info))
        else:
            user_info = yaml.safe_load(config_file.read_text())
            for param in ["url", "key", "secret"]:
                if param not in user_info:
                    raise AssertionError(f"Not found '{param}' in {config_file}")

        base_url = URL(user_info["url"]).resolve()
        api_endpoint = str(base_url / "wp-json/wp/v2")
        request_token_url = str(base_url / "oauth1/request")
        authorization_base_url = str(base_url / "oauth1/authorize")
        access_token_url = str(base_url / "oauth1/access")
        if "owner_key" not in user_info:
            oauth = OAuth1Session(user_info["key"], client_secret=user_info["secret"])
            fetch_response = oauth.fetch_request_token(request_token_url)
            resource_owner_key = fetch_response.get("oauth_token")
            resource_owner_secret = fetch_response.get("oauth_token_secret")

            authorization_url = oauth.authorization_url(authorization_base_url)
            print(authorization_url)
            verifier = input("Visit authorization_url. And input verifier.")
            # Using OAuth1Session
            oauth = OAuth1Session(
                user_info["key"],
                client_secret=user_info["secret"],
                resource_owner_key=resource_owner_key,
                resource_owner_secret=resource_owner_secret,
                verifier=verifier,
            )
            oauth_tokens = oauth.fetch_access_token(access_token_url)
            resource_owner_key = oauth_tokens.get("oauth_token")
            resource_owner_secret = oauth_tokens.get("oauth_token_secret")
            user_info["owner_key"] = resource_owner_key
            user_info["owner_secret"] = resource_owner_secret
            config_file.write_text(yaml.dump(user_info))
        else:
            resource_owner_key = user_info["owner_key"]
            resource_owner_secret = user_info["owner_secret"]
        self.api_endpoint = base_url / "wp-json/wp/v2"
        self.oauth = OAuth1Session(
            user_info["key"],
            client_secret=user_info["secret"],
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
        )

    def upload_image(self, image_path, name=None):
        if isinstance(image_path, str):
            image_path = Path(image_path)
        image_path = image_path.expanduser()
        suffix = image_path.suffix.replace(".", "")
        if name is None:
            name = image_path.name
        else:
            pathname = Path(name)
            if pathname.suffix.replace(".", "") != suffix:
                name = name + suffix
        headers = {
            "cache-control": "no-cache",
            "content-disposition": f"attachment; filename={name}",
            "content-type": f"image/{suffix}",
        }
        result = self.oauth.post(
            self.api_endpoint / "media", headers=headers, data=image_path.read_bytes()
        )
        return result

    def post_article(self, data):
        headers = {
            "cache-control": "no-cache",
        }
        result = self.oauth.post(
            self.api_endpoint / "posts", headers=headers, json=data
        )
        return result

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: thepoy
# @Email: thepoy@aliyun.com
# @File Name: gitee.py
# @Created: 2021-02-13 09:10:05
# @Modified: 2021-02-27 17:31:11

import os
import time
import requests

from typing import Optional, List, Dict, Tuple, Union
from base64 import b64encode

from timg.timglib.timg_api import Base
from timg.timglib.constants import GITEE
from timg.timglib.utils import Login, check_image_exists


class Gitee(Base):
    def __init__(self,
                 conf_file: Optional[str] = None,
                 auto_compress: bool = False):
        if not conf_file:
            super().__init__(GITEE)
        else:
            super().__init__(GITEE, conf_file)

        self.max_size = 1 * 1024 * 1024
        self.auto_compress: bool = auto_compress

        self.headers = {"Content-Type": "application/json;charset=UTF-8"}

        if self.auth_info:
            self.token: str = self.auth_info["token"]
            self.username: str = self.auth_info["username"]
            self.repo: str = self.auth_info["repo"]
            self.folder: str = self.auth_info["folder"]

    def login(self, token: str, username: str, repo: str, folder: str = "md"):
        auth_info = {
            "token": token,
            "username": username,
            "repo": repo,
            "folder": folder
        }
        self._save_auth_info(auth_info)

    @Login
    def upload_image(self, image_path: str) -> Union[str, dict]:
        image_path = self._compress_image(image_path)
        suffix = os.path.splitext(image_path)[-1]
        if suffix.lower() == '.apng':
            suffix = ".png"
        filename = f"{int(time.time() * 1000)}{suffix}"
        with open(image_path, "rb") as fb:
            url = self.base_url + filename
            data = {
                "access_token": self.token,
                "content": b64encode(fb.read()).decode("utf-8"),
                "message": "typora - " + filename,
            }
            resp = requests.post(url, headers=self.headers, json=data)
            if resp.status_code == 201:
                return resp.json()["content"]["download_url"]
            else:
                return {
                    "error": resp.json()["message"],
                    "status_code": resp.status_code,
                    "image_path": image_path,
                }

    @Login
    def upload_images(self, images_path: List[str]) -> List[str]:
        check_image_exists(images_path)

        self._check_images_valid(images_path)

        images_url = []
        for img in images_path:
            images_url.append(self.upload_image(img))

        for i in images_url:
            print(i)

        self._clear_cache()
        return images_url

    @Login
    def get_all_images_in_image_bed(self) -> Dict[str, str]:
        data = {
            "access_token": self.token,
        }
        resp = requests.get(self.base_url, headers=self.headers, json=data)
        return resp.json()

    @Login
    def get_all_images(self) -> List[Dict[str, str]]:
        images = []
        for file in self.get_all_images_in_image_bed():
            images.append({
                "sha": file["sha"],
                "delete_url": file["url"],
                "url": file["download_url"],
            })
        return images

    @Login
    def delete_image(self,
                     sha: str,
                     url: str,
                     message: str = "Delete pictures that are no longer used"):
        data = {"access_token": self.token, "sha": sha, "message": message}
        resp = requests.delete(url, headers=self.headers, json=data)
        return resp.status_code == 200

    @Login
    def delete_images(
            self,
            info: Tuple[str, str],
            message: str = "Delete pictures that are no longer used"):
        failed = []
        for sha, url in info:
            result = self.delete_image(sha, url, message)
            if not result:
                failed.append(sha)
        return failed

    @property
    def base_url(self) -> str:
        return "https://gitee.com/api/v5/repos/%s/%s/contents/%s/" % (
            self.username, self.repo, self.folder)

    def __str__(self):
        return "gitee.com"

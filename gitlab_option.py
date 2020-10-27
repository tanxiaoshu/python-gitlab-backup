#!/usr/bin/env python
# -*- coding: utf-8 -*-
# date: 2020-10-23
# author: TanXiaoshu
# E-mail: tanxiaoshu@vsoontech.com
# description: 同步gitlab代码
# python version 3.6 or newer
# install package python-gitlab-2.5.0,Gitpython-3.1.10
import json

import gitlab
import requests
from git import repo
import os


URL = "http://xxxxxx/"   # gitlab地址
TOKEN = "xxxxxx"  # gitlab生成的token
DIR = "/home/gitlab_backup/git-data/"


class gitlabOption():
    '''操作gitlab类方法'''
    def __init__(self):
        '''初始化连接'''
        self.gl = gitlab.Gitlab(URL, TOKEN)

    def get_group_project(self, group_id):
        group_projects = self.gl.groups.get(group_id)
        return group_projects

    def get_group(self):
        '''获取所有组，检查并创建组'''
        result = []
        groups = self.gl.groups.list(all=True)
        if os.path.exists(DIR):  # 备份目录是否存在
            os.chdir(DIR)
        else:
            os.makedirs(DIR)
            os.chdir(DIR)
        current_path_list = os.listdir(os.getcwd())
        for i in groups:
            if len(current_path_list) == 0:
                os.makedirs(DIR + i.name)
            else:
                if i.name not in current_path_list:
                    os.makedirs(DIR + i.name)
            result.append({"name": i.name, "id": i.id})
        return result

    def git_clone_project(self):
        '''按组克隆项目代码'''
        group_list = self.get_group()
        for group in group_list:
            os.chdir(DIR + group["name"])
            current_path_list = os.listdir(os.getcwd())
            group_projects = self.get_group_project(group["id"])
            if len(current_path_list) == 0:
                if group["id"] == 121:
                    for project in group_projects.projects.list():
                        repo.Repo.clone_from(url=project.ssh_url_to_repo, to_path=DIR + group["name"] + "/" + project.name)
            # else:
            #     for project in group_projects.projects.list():
            #         if project.name not in current_path_list:
            #             repo.Repo.clone_from(url=project.ssh_url_to_repo, to_path=DIR + group["name"] + "/" + project.name)
        return "源代码克隆成功"

    def git_pull_project(self):
        '''拉取更新代码'''
        group_list = self.get_group()
        for group in group_list:
            os.chdir(DIR + group["name"])
            current_path_list = os.listdir(os.getcwd())
            if group["name"] == "test2":
                for project in current_path_list:
                    os.chdir(DIR + group["name"] + "/" + project)
                    local_url = DIR + group["name"] + "/" + project
                    project_repo = repo.Repo(local_url)
                    branches = project_repo.remote().refs  # 获取所有分支
                    for item in branches:  # 遍历分支，拉取代码
                        # print(item.remote_head)
                        if item.remote_head != "HEAD":
                            pro = project_repo.git.checkout(item.remote_head)
                            # print("==>", pro)
                            res = project_repo.git.pull()
                            # print(res)
        return "源代码备份成功"

    def send_message(self, result):
    '''企业微信接口'''
        url = "http://xxx.xxx.xxx.xxx"
        params = {
            "AppId": xxxx,
            "AppKey": "xxxx",
            "btntxt": "查看详情",
            "description": result,
            "title": "gitlab源代码备份",
            "touser": ["tan"],
            "url": "http://xxx.xxx.xxx.xxx/K8S-POD-status.txt"
        }
        req = requests.post(url, data=json.dumps(params))


if __name__ == "__main__":
    gitlabOpt = gitlabOption()
    try:
        gitlabOpt.git_clone_project()
        gitlabOpt.git_pull_project()
        result = "源代码备份成功"
    except Exception as e:
        result = "源代码备份失败: %s" % str(e)
        print(result)
    gitlabOpt.send_message(result)

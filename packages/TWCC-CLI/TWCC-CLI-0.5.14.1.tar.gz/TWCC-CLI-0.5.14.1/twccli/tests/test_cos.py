# -*- coding: utf-8 -*-
from click.testing import CliRunner
#from ..twcc import Session2
#from ..twcc.util import isNone
import os
import re
import click
import json
from ..twccli import cli
import pytest
import uuid
import subprocess
import random


class TestCosLifecyc:

    def _loadSession(self):
        self.runner = CliRunner()

    def _loadParams(self):
        rand = random.randint(0, 1000)
        self.bk_name = "bucket{}".format(str(rand))
        self.dir = "dir_{}".format(str(rand))

    def __run(self, cmd_list):
        result = self.runner.invoke(cli, cmd_list)
        # print(result.output)
        #assert result.exit_code == 0
        return result.output

    def _create_bucket(self, bk):
        cmd_list = "mk cos -bkt {}".format(bk)
        print(cmd_list)
        self.create_out = self.__run(cmd_list.split(u" "))

    def _list_bucket_after_create(self):
        cmd_list = "ls cos -json"
        print(cmd_list)
        self.list_out = self.__run(cmd_list.split(u" "))
        print(self.list_out)
        out = json.loads(self.list_out)

        flag = False
        for ele in out:
            if ele['Name'] == self.bk_name:
                flag = True

        assert flag

    def _del_bucket_no_r(self, bkt):
        cmd_list = "rm cos -bkt {} -f".format(bkt)
        print(cmd_list)
        out = self.__run(cmd_list.split(u" "))

    def _del_bucket(self, bkt):
        cmd_list = "rm cos -bkt {} -r -f".format(bkt)
        print(cmd_list)
        out = self.__run(cmd_list.split(u" "))

    def _list_bucket_after_delete(self):
        cmd_list = "ls cos -json"
        print(cmd_list)
        self.list_out = self.__run(cmd_list.split(u" "))
        out = json.loads(self.list_out)

        flag = True
        for ele in out:
            if ele['Name'] == self.bk_name:
                flag = False

        assert flag

    def _upload_files(self):
        cmd_list = "cp cos -upload -src {} -dest {} -r".format(
            self.upload_dir, self.bk_name)
        print(cmd_list)
        out = self.__run(cmd_list.split(u" "))

    def test_create_bucket(self):
        self._loadSession()
        self._loadParams()
        self._create_bucket(self.bk_name)
        self._list_bucket_after_create()
        self._del_bucket(self.bk_name)
        self._list_bucket_after_delete()

    def _create_hierarchy_files(self, dir):
        cmd1 = ["mkdir", dir]
        cmd2 = ["touch", dir + "/1.txt", dir + "/2.txt"]
        cmd3 = ["mkdir", dir + "/subdir"]
        cmd4 = ["touch", dir + "/subdir/3.txt", dir + "/subdir/4.txt"]

        p = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
        p.communicate()
        p = subprocess.Popen(cmd2, stdout=subprocess.PIPE)
        p.communicate()
        p = subprocess.Popen(cmd3, stdout=subprocess.PIPE)
        p.communicate()
        p = subprocess.Popen(cmd4, stdout=subprocess.PIPE)
        p.communicate()

    def _upload_files(self, bk, dir):
        cmd_list = "cp cos -upload -src {} -dest {} -r".format(dir, bk)
        print(cmd_list)
        out = self.__run(cmd_list.split(u" "))
    def _op_folder(self, bk, dir, op):
        cmd_list = "cp cos -bkt {} -dir {} -sync {}".format(bk, dir, op)
        print(cmd_list)
        out = self.__run(cmd_list.split(u" "))

    def _download_files(self, bk, dir):
        cmd_list = "cp cos -download -src {} -dest {} -r".format(bk, dir)
        print(cmd_list)
        out = self.__run(cmd_list.split(u" "))

    def _del_isu85_files(self):
        dir = self.isu85_Dir.replace("./", "")
        cmd = ["rm", "-rf", self.isu85_Dir]
        subprocess.run(cmd)
    def _check_isu178_upload_files(self, download_path, check_res):
        response = subprocess.check_output('ls {} | wc -l'.format(download_path), shell=True).decode('utf8').strip()
        return True if response == check_res else False
    def _check_isu85_upload_files(self):
        '''
        localList = []
        for localF in out.splitlines():
            localList.append(localF)
            print('local {}'.format(localF))
        '''

        # ================

        cmd_remote = "ls cos -n {} -json".format("bk123")
        print(cmd_remote)
        self.list_out = self.__run(cmd_remote.split(u" "))
        out2 = json.loads(self.list_out)
        print(out2)

        #flag = True
        remoteList = []
        for ele in out2:
            str = ele['Key']
            remoteList.append(str)
            print('remote = {}'.format(str))

        for root, dirs, files in os.walk('./updir'):
            for name in files:
                print("file={}".format(os.path.join(root, name)))
                scanPath = os.path.join(root, name)
                scanPath = scanPath.replace('./', '')
                if scanPath in remoteList:
                    print('yes {}'.format(scanPath))
                else:
                    print('no {}'.format(scanPath))

        assert False

    def _mk_download_dir(self, downDir):
        cmd = ["mkdir", downDir]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        p.communicate()

    def _remove_file(self, fn):
        cmd = ["rm", fn]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        p.communicate()

    def _remove_dir(self, updir, downdir):
        cmd1 = ["rm", "-rf", updir]
        cmd2 = ["rm", "-rf", downdir]
        print(cmd1)
        p = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
        p.communicate()
        print(cmd2)
        p = subprocess.Popen(cmd2, stdout=subprocess.PIPE)
        p.communicate()

    def _create_download_dir(self, dir):
        cmd = ["mkdir", dir]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        p.communicate()

    def _create_upload_file(self, file):
        cmd = ["touch", file]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        p.communicate()

    def _remove_upload_file(self, file):
        cmd = ["rm", file]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        p.communicate()

    def _upload_single_file_by_fn(self, src, bk, fn):
        cmd_list = "cp cos -bkt {} -dir {} -fn {} -sync to-cos".format(bk, src, fn)
        print(cmd_list)
        out = self.__run(cmd_list.split(u" "))

    def _upload_single_file(self, bk, file):

        cmd_list = "cp cos -bkt {} -fn {} -sync to-cos".format(bk, file)
        print(cmd_list)
        out = self.__run(cmd_list.split(u" "))

    def _download_single_file(self, bk, key, downdir):

        cmd_list = "cp cos -bkt {} -dir {} -okey {} -sync from-cos".format(
            bk, downdir, key)
        print(cmd_list)
        out = self.__run(cmd_list.split(u" "))

    def _download_specific_dir(self, bk, dest, downdir):

        cmd_list = "cp cos -bkt {} -dir {} -okey {} -sync from-cos".format(
            bk, dest, downdir)
        print(cmd_list)
        out = self.__run(cmd_list.split(u" "))

    def _mk_146_upload_file(self, dir):
        cmd1 = ["mkdir", dir]
        cmd2 = ["mkdir", dir + "/subdir"]
        cmd3 = ["touch", dir+"/1.txt", dir+"/2.txt"]
        cmd4 = ["touch", dir + "/subdir/1.txt", dir + "/subdir/2.txt"]

        cmd_list = [cmd1, cmd2, cmd3, cmd4]

        for cmd in cmd_list:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            p.communicate()

    def _issue_104(self):
        rand = random.randint(0, 1000)
        bk_isu104 = "bk_isu104_{}".format(str(rand))
        isu104_upDir = "./isu104_up_{}".format(str(rand))
        isu104_downDir = "./isu104_down_{}".format(str(rand))
        downdir = "subdir"
        self._loadSession()
        self._create_bucket(bk_isu104)

        self._mk_download_dir(isu104_downDir)
        self._create_hierarchy_files(isu104_upDir)
        self._upload_files(bk_isu104, isu104_upDir)
        self._download_specific_dir(bk_isu104, isu104_downDir, downdir)

        self._remove_dir(isu104_upDir, isu104_downDir)
        self._remove_dir(downdir, "")
        self._del_bucket(bk_isu104)

    def _issue_80(self):
        rand = random.randint(0, 1000)
        bk_isu80 = "bk_isu80_{}".format(str(rand))
        isu80_upDir = "./isu80_up_{}".format(str(rand))
        isu80_downDir = "./isu80_down_{}".format(str(rand))

        self._loadSession()
        self._create_bucket(bk_isu80)

        self._create_hierarchy_files(isu80_upDir)
        self._upload_files(bk_isu80, isu80_upDir)
        self._mk_download_dir(isu80_downDir)
        self._download_files(bk_isu80, isu80_downDir)
        self._remove_dir(isu80_upDir, isu80_downDir)
        self._del_bucket(bk_isu80)

    def _issue_103(self):
        rand = random.randint(0, 1000)
        bk_isu103 = "bk_isu103_{}".format(str(rand))
        isu103_upDir = "./isu103_up_{}".format(str(rand))
        isu103_downDir = "./isu103_down_{}".format(str(rand))
        isu103_file = "./isu103_{}.txt".format(str(rand))
        self._loadSession()
        self._create_bucket(bk_isu103)
        self._create_upload_file(isu103_file)
        self._create_download_dir(isu103_downDir)
        self._upload_single_file(bk_isu103, isu103_file)
        self._download_single_file(bk_isu103, isu103_file, isu103_downDir)
        self._del_bucket(bk_isu103)
        self._remove_dir(isu103_upDir, isu103_downDir)
        self._remove_upload_file(isu103_file)

    def _issue_85(self):
        rand = random.randint(0, 1000)
        bk_isu85 = "bk_isu85_{}".format(str(rand))
        isu85_Dir = "./isu85_{}".format(str(rand))

        self._loadSession()
        self._create_bucket(bk_isu85)

        self._create_hierarchy_files(isu85_Dir)
        self._upload_files(bk_isu85, isu85_Dir)
        self._del_bucket(bk_isu85)
        self._remove_dir(isu85_Dir, "")

    def _issue_78(self):
        rand = random.randint(0, 1000)
        bk_isu78 = "bk_isu78_{}".format(str(rand))
        isu78_Dir = "./isu78_{}".format(str(rand))

        self._loadSession()

        self._create_bucket(bk_isu78)
        self._create_hierarchy_files(isu78_Dir)
        self._upload_files(bk_isu78, isu78_Dir)
        self._del_bucket(bk_isu78)
        self._remove_dir(isu78_Dir, "")

    def _issue_115(self):
        rand = random.randint(0, 1000)
        bk_isu105 = "bk_isu105_{}".format(str(rand))
        isu105_Dir = "./isu105_{}/".format(str(rand))
        self._loadSession()
        self._create_bucket(bk_isu105)

        self._create_hierarchy_files(isu105_Dir)
        self._upload_files(bk_isu105, isu105_Dir)
        self._del_bucket(bk_isu105)
        self._remove_dir(isu105_Dir, "")

    def _issue_132(self):

        bk_isu132rel = "bk132rel{}".format(str(uuid.uuid1()).split("-")[0])
        bk_isu132abs = "bk132abs{}".format(str(uuid.uuid1()).split("-")[0])
        isu132_relDir = "./isu132_{}/".format(str(uuid.uuid1()).split("-")[0])
        isu132_absDir = os.path.abspath(isu132_relDir)

        isu132_relfn = "rel.txt"
        isu132_absfn = "abs.txt"
        isu132_onlyfn = "onlyfn.txt"
        # upload by relative path

        self._loadSession()
        self._create_bucket(bk_isu132rel)
        self._create_hierarchy_files(isu132_relDir)
        self._upload_files(bk_isu132rel, isu132_relDir)

        # upload by abs path

        self._create_bucket(bk_isu132abs)
        self._upload_files(bk_isu132abs, isu132_absDir)

        # upload by src , single file

        self._create_upload_file("./"+isu132_relfn)
        self._create_upload_file("./"+isu132_absfn)
        self._upload_single_file_by_fn(os.getcwd(), bk_isu132rel, isu132_relfn)
        self._upload_single_file_by_fn("./", bk_isu132rel, isu132_absfn)
        self._remove_file("./"+isu132_relfn)
        self._remove_file("./"+isu132_absfn)

        # upload onlyby fn
        self._loadSession()
        self._create_bucket(bk_isu132rel)
        self._create_upload_file("./"+isu132_onlyfn)
        self._upload_single_file_by_fn("", bk_isu132rel, isu132_onlyfn)

        # delete file & bucket

        self._del_bucket(bk_isu132abs)
        self._del_bucket(bk_isu132rel)
        self._remove_file("./"+isu132_onlyfn)
        self._remove_dir(isu132_relDir, "")

    def _issue_146(self):
        bk_isu146 = "bk146{}".format(str(uuid.uuid1()).split("-")[0])
        isu146_upDir = "./isu146_{}/".format(str(uuid.uuid1()).split("-")[0])
        isu146_downDir = "./isu146down_{}/".format(
            str(uuid.uuid1()).split("-")[0])
        # make upload file
        self._loadSession()
        self._create_bucket(bk_isu146)
        self._mk_146_upload_file(isu146_upDir)
        self._create_download_dir(isu146_downDir)
        self._upload_files(bk_isu146, isu146_upDir)
        self._download_specific_dir(bk_isu146, isu146_downDir, isu146_upDir)

        self._del_bucket(bk_isu146)
        self._remove_dir(isu146_downDir, isu146_upDir)

    def _issue_147(self):
        bk_isu147 = "bk147{}".format(str(uuid.uuid1()).split("-")[0])
        self._loadSession()
        self._create_bucket(bk_isu147)
        self._del_bucket_no_r(bk_isu147)

    def _issue_178(self):
        bk_isu178 = "bk178_{}".format(str(uuid.uuid1()).split("-")[0])
        isu178_upload_folder = 'isu178_upload_folder'
        isu178_download_folder = 'isu178_download_folder'
        self._loadSession()
        self._create_bucket(bk_isu178)
        self._create_download_dir(isu178_upload_folder)
        self._create_download_dir(isu178_download_folder)
        [self._create_upload_file('{}/{}'.format(isu178_upload_folder,'isu178_'+str(i))) for i in range(1001)]
        self._op_folder(bk_isu178,isu178_upload_folder,'to-cos')
        self._op_folder(bk_isu178,isu178_download_folder,'from-cos')
        
        if self._check_isu178_upload_files('./'+os.path.join(isu178_download_folder,isu178_upload_folder),'1001'):
            assert True 
        else:
            assert False
        self._remove_dir(isu178_download_folder, isu178_upload_folder)
        self._del_bucket(bk_isu178)

        
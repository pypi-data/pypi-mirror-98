# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import re
import boto3
import click
from distutils.dir_util import mkpath
from botocore.exceptions import ClientError
from ..clidriver import ServiceOperation
from termcolor import colored
from terminaltables import AsciiTable
from tqdm import tqdm
from twccli.twcc.session import Session2
from twccli.twcc.util import sizeof_fmt, pp, isNone
from dateutil import tz
from datetime import datetime
import subprocess


class S3():
    def __init__(self):
        """ Initilaize information for s3 bucket
        """
        # The setting for connect to s3 bucket
        self.service_name = 's3'
        self.endpoint_url = "cos.twcc.ai"
        self.new_files = []
        self.new_bucket = []
        self.twcc = ServiceOperation()
        session = Session2()
        self.access_key = session.twcc_s3_access_key
        self.secret_key = session.twcc_s3_secret_key

        # Make sure there are value input here
        if not self.access_key or not self.secret_key:
            raise Exception("No key entered by user")

        session = boto3.session.Session()
        self.s3_cli = session.client(service_name=self.service_name,
                                     aws_access_key_id=self.access_key,
                                     aws_secret_access_key=self.secret_key,
                                     endpoint_url='https://' + self.endpoint_url,
                                     verify=False)

    def list_bucket(self):
        """ Listing all the bucket for S3 directory

            :return            : List all S3 buckets
        """
        response = self.s3_cli.list_buckets()
        res = []
        to_zone = tz.tzlocal()

        for x in response['Buckets']:
            ele = {}
            for y in x:
                if y == u'CreationDate':
                    ele[y] = x[y].astimezone(
                        to_zone).strftime("%m/%d/%Y %H:%M:%S")
                else:
                    ele[y] = x[y]
            res.append(ele)
        return res

    def list_dir(self, bucket_name, directory, downdir):
        # list dir in cloud
        res = self.list_object(bucket_name)

        dir_set = set()
        for i in res:
            str = i['Key']
            ele = str.split('/')
            for ee in ele[:-1]:
                dir_set.add(ee)

        if downdir.startswith('./'):
            downdir = downdir.replace("./", "")

        if downdir.endswith('/'):
            downdir = downdir[:-1]

        if downdir in dir_set:
            for i in res:
                if i['Key'].find(downdir) > -1:
                    # print("{} in".format(i['Key']))
                    last_idx = i['Key'].rfind('/')
                    file_name = os.path.join(directory+'/', i['Key'])
                    file_dir = os.path.join(directory+'/', i['Key'][:last_idx])
                    cmd = ["mkdir", "-p", file_dir]
                    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                    p.communicate()
                    # file_path = os.path.join(directory+'/', i['Key'])
                    key = i['Key'][last_idx+1:]
                    response = self.s3_cli.download_file(
                        bucket_name, i['Key'], file_name)
        else:
            print("Can not find {} in {}".format(downdir, bucket_name))
            return

    def put_obj_acl(self, key , bkt, is_public):
        acl_string ='private'
        if is_public:
            acl_string ='public-read'

        res =self.s3_cli.put_object_acl(ACL=acl_string,
               Bucket=bkt,
               Key = key)

    def is_key_public(self, key, bkt):
        date = ''
        publicFlag = 'N'
        res = self.s3_cli.get_object_acl(Bucket=bkt, Key=key)
        # get public flag ===================
        for grants in res['Grants']:
            for grantee in grants['Grantee']:
                if grantee == "URI":
                    if grants['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/global/AllUsers':
                        publicFlag = 'Y'

        # get date ===========================
        for metadata in res['ResponseMetadata']:
            date = res['ResponseMetadata']['HTTPHeaders']['date']

        # combine return json string ====
        ret = []
        ret.append({"okey": key,
                            "time": date,
                            "is_public": publicFlag})

        return ret
    def object_acl(self,bucket, key):

        #object_acl = self.s3res.ObjectAcl(bucket, key)
        #response = object_acl.put(ACL='public-read')
        res = self.s3_cli.get_object_acl( Bucket=bucket, Key=key)

        #{'Grantee': {'Type': 'Group', 'URI': 'http://acs.amazonaws.com/groups/global/AllUsers'}, 'Permission': 'READ'}
    def list_object(self, bucket_name):
        """ Listing all the file insife of S3 bucket.

            :param bucket_name : Unique string name
            :return            : List all object inside of S3 bucket.
        """
        res_list = []
        NextMarker = ''
        while True:
            res = self.s3_cli.list_objects(Bucket=bucket_name,Marker=NextMarker)
            res_list.append(res)
            if 'NextMarker' in res:
                NextMarker = res['NextMarker']
            else:
                break
        
        # res = self.s3_cli.list_objects(Bucket=bucket_name)
        not_show = set(('ETag', 'Owner', 'StorageClass'))
        tmp = []
        to_zone = tz.tzlocal()
        for res in res_list:
            if not 'Contents' in res:
                continue
            else:
                for ele in res['Contents']:
                    if isNone(ele):
                        continue#return []
                    data = {}
                    for key in ele:
                        if not key in not_show:
                            if key == "Size":
                                data[key] = sizeof_fmt(ele[key])
                            elif key == "LastModified":
                                data[key] = ele[key].astimezone(
                                    to_zone).strftime("%m/%d/%Y %H:%M:%S")
                            else:
                                data[key] = ele[key]
                    tmp.append(data)
        if tmp:
            return tmp
        else:
            return None

    def upload_file(self, bucket_name=None, key=None):
        try:
            self.s3_cli.upload_file(remotePath, bucket_name, key)
        except ClientError as e:
            print(e)
            return False

    def upload_bucket(self, file_name=None, bucket_name=None, key=None, path=None, r=False):
        """ Upload to S3

            :param file_name         : The name of the upload file
            :param path              : The path for the files, r must set ot True
            :param bucket_name       : The bucket name
            :param key               : The file name shows inside the bucket
            :param r                 : Setting for recursive
            :return                  : True if success upload file to S3 bucket
        """

        if r == True:
            if os.path.isdir(path):
                cmd = ['find', path]
                # res =subprocess.run(cmd, capture_output=True)
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                out, err = p.communicate()

                for singleFilePath in out.decode('utf-8').split("\n"):
                    if os.path.isdir(singleFilePath) == False and len(singleFilePath) > 0:
                        if os.path.isabs(path) == False:
                            singleFilePath = singleFilePath.replace("./", "")
                            localPath = os.path.abspath(
                                os.path.dirname(path))+'/' + singleFilePath

                            remotePath = os.path.dirname(
                                path)+'/'+singleFilePath
                            remotePath = remotePath.replace("./", "")
                            if remotePath.startswith('/'):
                                remotePath = remotePath[1:]
                        else:
                            localPath = singleFilePath
                            remotePath = singleFilePath.replace(
                                os.path.split(path)[0]+'/', '')

                        try:
                            self.s3_cli.upload_file(
                                localPath, bucket_name, remotePath)
                        except ClientError as e:
                            print(e)
                            return False

            else:
                raise Exception("Path: {} is not founded. ".format(path))
        else:
            try:
                response = self.s3_cli.upload_file(file_name, bucket_name, key)
                print("Successfully upload file : ", key)
            except ClientError as e:
                print(e)
                return False
            return True

    def download_file(self, bucket_name=None, key=None, file_name=None, path=None):
        a = self.list_object(bucket_name)

        for i in a:
            ff_name = os.path.join(path+'/', i['Key'])
            if ff_name.find(key) > 0:
                self.s3_cli.download_file(bucket_name, i['Key'], ff_name)

    def download_bucket(self, bucket_name=None, key=None, file_name=None, path=None, r=False):
        """ Download from S3

            :param bucket_name       : The bucket name
            :param key               : The file name shows inside the bucket
            :param path              : The path for the files, r must set ot True
            :param file_name         : The name of the download file
            :param r                 : Setting for recursive
            :return            : True if success upload file to S3 bucket
        """
        if r:
            # checking for download path exists
            if os.path.isdir(path):
                # get the list of objects inside the bucket
                # a = self.list_object(bucket_name)[1:]
                all_objs = self.list_object(bucket_name)

                # loop through all the objects
                for obj in all_objs :
                    full_path = os.path.abspath(path)
                    if re.match("^\/", obj['Key']):
                        ff_name = os.path.join(full_path, obj['Key'][1:])
                    else:
                        ff_name = os.path.join(full_path, obj['Key'])

                    dest_path = os.path.abspath(ff_name)
                    # check if the download folder exists
                    if not os.path.isdir(dest_path):
                        mkpath(os.path.sep.join(dest_path.split(os.path.sep)[:-1]))
                    # download to the correct path
                    self.s3_cli.download_file(bucket_name, obj['Key'], ff_name)
            else:
                raise Exception("Path: '{}' is not founded. ".format(path))
        else:
            try:
                if not file_name.endswith('/'):
                    check_path = "/".join(file_name.split('/')[:-1])

                if not os.path.isdir(check_path):
                    os.mkdir(check_path)

                response = self.s3_cli.download_file(
                    bucket_name, key, file_name)
                print("Successfully download file : ", file_name)
            except ClientError as e:
                print("ERROR during download : ", e)
                return False
            return True

    def create_bucket(self, bucket):
        """ Create an S3 bucket

            :param bucket_name: Unique string name
            :return           : True if bucket is created, else False
        """
        try:
            self.s3_cli.create_bucket(Bucket=bucket)
            self.new_bucket.append(bucket)
            print("Successfully create bucket :", self.c_t(bucket))
        except ClientError as e:
            print("ERROR during create : ", e)
            return False
        return True

    def del_bucket(self, bucket_name, recursive=False):
        """ Delete a bucket from S3

            :param bucket_name: Unique string name
            :param recursive: recursive or no
            :return: True if bucket is deleted, else False
        """
        if recursive == True:
            retKeys = self.list_object(bucket_name)
            if retKeys != None:
                for i in self.list_object(bucket_name):
                    self.del_object(bucket_name=bucket_name,
                                    file_name=i['Key'])
        res = self.s3_cli.delete_bucket(Bucket=bucket_name)
        print("Successfully delete bucket :", bucket_name)

    def del_object(self, bucket_name, file_name):
        """ Delete a file from S3

            :param bucket_name: Unique string name
            :param file_name  : Unique string name
            :return           : True if object is deleted, else False
        """
        res = self.s3_cli.delete_object(Bucket=bucket_name,
                                        Key=file_name)

    # def test_table(self, table_data):
    #     """ Testing showing table
    #     """
    #     table = AsciiTable(table_data)
    #     print(table.table)

    def c_t(self, txt, color="red"):
        return colored(txt, color)

    def check_4_bucket(self, bucket_name):
        try:
            res = self.s3_cli.head_bucket(Bucket=bucket_name)
        except ClientError as e:
            return False
        return True

    def list_files_v2(self, bucket_name, delimiter='', prefix=''):
        try:
            res = self.s3_cli.list_objects_v2(
                Bucket=bucket_name, Delimiter=delimiter, Prefix=prefix)
            return [now_dict['Key'] for now_dict in res['Contents']]
            # for now_dict in res['Contents']:
            #    print(now_dict['Key'])
        except ClientError as e:
            return False
        return True

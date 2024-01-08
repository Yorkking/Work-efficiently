# coding:utf-8
import time
import imaplib
import email
import os
import datetime
from email.header import decode_header
import re


class IMAP_Downemail(object):
    """
    imap邮箱下载附件(腾讯企业邮箱测试通过)
    """    
    def __init__(self, account, pwd, serverurl, savedir, startdate, enddate, subject_regular_rule, file_regular_rule, exts=['.xls', '.xlsx', '.jpg', '.png', '.pptx']):
        """
        init
        :param account:   邮箱账户
        :param pwd:       密码
        :param serverurl: 接收服务器地址
        :param savedir:   文件保存路径
        :param startdate: 邮件开始日期
        :param enddate:   邮件结束日期
        :param exts:      附件拓展名
        """
        self._account = account
        self._pwd = pwd
        self._serverurl = serverurl
        self._savedir = savedir
        self._startdate = startdate
        self._enddate = enddate
        self._exts = exts
        self._subject_regular_rule = subject_regular_rule
        self._file_regular_rule = file_regular_rule

    def __getEmailattachment(self, msg):
        """
        下载邮件中的附件
        """
        attachments = []

        # 获取邮件主题
        _subject = msg.get('Subject')
        subject = decode_header(_subject)[0][0].decode(
            decode_header(_subject)[0][1])

        # 过滤符合规则的主题
        _file_name = ''
        if re.match(self._subject_regular_rule, subject) is None:
            print("%s : subject is not legal!!" % (subject))
            return attachments
        _file_name = subject

        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            fileName = part.get_filename()

            # 如果文件名为纯数字、字母时不需要解码，否则需要解码
            try:
                fileName = decode_header(fileName)[0][0].decode(
                    decode_header(fileName)[0][1])
            except:
                pass

            # 只获取指定拓展名的附件
            extension = os.path.splitext(os.path.split(fileName)[1])[1]
            if extension not in self._exts:
                continue

            # 筛选符合条件的文件
            if re.match(self._file_regular_rule, fileName) is None:
                print("%s : filename is not legal!!" % (fileName))
                fileName = subject + extension
                print("replaced filename: %s" % (fileName))

            # 如果获取到了文件，则将文件保存在指定的目录下
            if fileName:
                if not os.path.exists(self._savedir):
                    os.makedirs(self._savedir)
                filePath = os.path.join(self._savedir, fileName)
                if os.path.exists(filePath):
                    continue
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
                attachments.append(fileName)

        return attachments

    def scanDown(self, process_fun=None):
        if process_fun:
            process_fun("当前邮箱：{}".format(self._account))

        # 连接到qq企业邮箱，其他邮箱调整括号里的参数
        conn = imaplib.IMAP4_SSL(self._serverurl, 993)

        if process_fun:
            process_fun("身份认证...")
        try:
            # 用户名、密码，登陆
            conn.login(self._account, self._pwd)
            login_success = True
        except:
            login_success = False

        if login_success:
            if process_fun:
                process_fun("邮箱{}登录成功！".format(self._account))

            # 选定一个邮件文件夹
            # 收件箱默认名称是"INBOX"
            # 可以用conn.list()查看都有哪些文件夹
            conn.select("INBOX")

            # 提取文件夹中所有邮件的编号
            resp, mails = conn.search(None, 'ALL')

            # 邮件编号列表
            msgList = mails[0].split()

            # 从最近的邮件开始获取
            for i in reversed(range(len(msgList))):
                try:
                    resp, data = conn.fetch(msgList[i], '(RFC822)')
                    emailbody = data[0][1]
                    mail = email.message_from_bytes(emailbody)

                    # 解析邮件日期
                    try:
                        mail_date = time.strptime(
                            mail.get("Date")[0:24], '%a, %d %b %Y %H:%M:%S')  # 格式化收件时间
                    except:
                        mail_date = time.strptime(
                            mail.get("Date"), '%d %b %Y %H:%M:%S +0800')  # 格式化收件时间
                    mail_date = time.strftime("%Y%m%d", mail_date)

                    startdate = self._startdate
                    stopdate = self._enddate

                    if mail_date == (datetime.datetime.strptime(startdate, '%Y%m%d') - datetime.timedelta(days=1)).strftime('%Y%m%d'):
                        break

                    if mail_date == (datetime.datetime.strptime(startdate, '%Y%m%d') - datetime.timedelta(days=3)).strftime('%Y%m%d'):
                        break

                    if (mail_date < startdate) | (mail_date > stopdate):
                        continue

                    # 获取附件
                    attachments = self.__getEmailattachment(mail)
                    for attachment in attachments:
                        if process_fun:
                            process_fun("已下载文件：{}".format(attachment))
                except:
                    continue

            conn.close()
            conn.logout()
        else:
            if process_fun:
                process_fun("邮箱{}登录失败！".format(self._account))


if __name__ == '__main__':
    def process_msg(msg):
        print(msg)

    # 邮箱账号列表
    account_list = [
        {
            "email": "*****",  # 邮箱
            "password": "*******",  # 授权密码
            "server": "*********"  # 服务器地址
        }
    ]

    # 文件保存目录
    _dir = r"./intro"

    # 邮件开始日期和结束日期
    startdate = "20240107"
    enddate = "20240111"

    # 过滤邮件主题和邮件附件规则
    subject_regular_rule = r'regular rule'
    file_regular_rule = r'regular rule'

    # 下载
    for account in account_list:
        _email = account['email']
        _password = account['password']
        _server = account['server']
        etool = IMAP_Downemail(_email, _password, _server,
                               _dir, startdate, enddate, subject_regular_rule, file_regular_rule)
        etool.scanDown(process_msg)

    print('Done.')

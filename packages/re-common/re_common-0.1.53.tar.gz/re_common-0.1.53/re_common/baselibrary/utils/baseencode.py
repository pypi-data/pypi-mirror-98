class BaseEncode(object):

    def __init__(self):
        pass

    @classmethod
    def get_byte_md5_value(cls, bytes):
        """
        获得byte md5值
        :param bytes:需要操作的二进制
        :return:
        """
        import hashlib
        myMd5 = hashlib.md5(bytes)
        myMd5_Digest = myMd5.hexdigest()
        return myMd5_Digest

    @classmethod
    def get_md5_value(cls, src):
        """
        获得字符串md5值
        :param src:需要操作的字符串
        :return:
        """
        import hashlib
        myMd5 = hashlib.md5()
        myMd5.update(src.encode("utf8"))
        myMd5_Digest = myMd5.hexdigest()
        return myMd5_Digest

    @classmethod
    def get_md5_value_16bit(cls, src):
        """
        获取16位md5
        :param src:
        :return:
        """
        return cls.get_md5_value(src)[8:-8]

    @classmethod
    def get_byte_md5_value_16bit(cls, bytes):
        """
        获取16位md5
        :param bytes:
        :return:
        """
        return cls.get_byte_md5_value(bytes)[8:-8]

    @classmethod
    def get_sha1_value(cls, src):
        """
         获得字符串sha1值
        :param src:
        :return:
        """
        import hashlib
        mySha1 = hashlib.sha1()
        mySha1.update(src)
        mySha1_Digest = mySha1.hexdigest()
        return mySha1_Digest

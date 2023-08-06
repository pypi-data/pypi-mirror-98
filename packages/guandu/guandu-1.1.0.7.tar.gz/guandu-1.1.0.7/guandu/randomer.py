from uuid import uuid4


def get_random_code(code_name: str, count: int) -> str:
    """
    获取随机编码
    :param code_name: 自定义字符串
    :param count: 自定义随机位数
    :return:
    """

    code = f"{code_name}{str(uuid4()).replace('-', '')[:count]}"

    return code


if __name__ == '__main__':
    print(get_random_code("JD", 7))

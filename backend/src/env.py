# 从.env文件中读取环境变量，并提供一个函数用于获取特定环境变量的值
env_dict = {}

with open('../../.env') as file:
    for line in file:
        # Strip leading and trailing whitespaces and split by '='
        key, value = line.strip().split('=')
        # Add the key-value pair to the dictionary
        env_dict[key] = value


def getEnv(key):
    return env_dict[key]


if __name__ == '__main__':
    print(getEnv('OPENAI_KEY'))

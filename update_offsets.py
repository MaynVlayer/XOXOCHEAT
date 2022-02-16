import requests

# url = https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.toml


def update_offsets(file_name='offsets.py'):
    try:
        request = requests.get(
            'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.toml')

        text = request.text.replace('[signatures]', '').replace('[netvars]', '')

        with open('offsets.py', 'wt') as f:
            f.write(text)
        
        return True
    except Exception as e:
        return False


if __name__ == '__main__':
    update_offsets()
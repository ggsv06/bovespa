import json
import os

def create_json_config(email, remetente, token, nsave):
    # Path do arquivo
    appdata_path = os.getenv('APPDATA')
    file_path = os.path.join(appdata_path, 'bov_data.json')
    # Se o arquivo existe, leia-o, caso contrário, crie dic base
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                data_dic = json.load(f)
            except:
                data_dic = {
                    'config': {},
                    'menu': {}
                }
    else:
        data_dic = {
            'config': {},
            'menu': {}
        }
    try:
        data = {
            'email': email,
            'remetente': remetente,
            'token': token,
        }
        data_dic['config'][nsave] = data
        # Salvar arquivo
        try:
            with open(file_path, "w") as f:
                json.dump(data_dic, f, indent=4)
            return True
        except:
            return False
    except:
        return False

def create_json_menu(nome1, nome2, valor1, valor2, taxa, nsave):
    appdata_path = os.getenv('APPDATA')
    file_path = os.path.join(appdata_path, 'bov_data.json')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                data_dic = json.load(f)
            except:
                data_dic = {
                    'config': {},
                    'menu': {}
                }
    else:
        data_dic = {
            'config': {},
            'menu': {}
        }
    try:
        data = {
            'nome1': nome1,
            'nome2': nome2,
            'valor1': valor1,
            'valor2': valor2,
            'taxa': taxa
        }
        data_dic['menu'][nsave] = data
            # Salvar arquivo
        try:
            with open(file_path, 'w') as f:
                json.dump(data_dic, f, indent=4)
            return True
        except:
            return False
    except:
        return False

def read_json(mode, nsave):
    appdata_path = os.getenv('APPDATA')
    file_path = os.path.join(appdata_path, 'bov_data.json')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            dic = json.load(f)
            return dic[mode][nsave]
    else:
        return False

 
if __name__ == '__main__':
    create_json_config('ggsv', 'qwerty', 123, 'parte1')
    create_json_menu('brap4', 'vale3', 15, 40, 10, 'parte1')
    read_json('menu', 'parte1')
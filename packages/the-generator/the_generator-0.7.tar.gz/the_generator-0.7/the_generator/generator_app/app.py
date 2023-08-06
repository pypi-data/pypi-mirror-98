import pathlib
import os
import jsonpickle
import copy
import re
from jinja2 import Template

LIST_PYTHON_FILE = ['models', 'forms', 'tables', 'apps', 'admin', 'views', 'urls']


def remove_read_only_attribute(data_json):
    print(data_json)
    result_dict: dict = copy.deepcopy(data_json)
    result_list: list = list()
    attributes = result_dict['attributes']
    for index in range(len(result_dict['attributes'])):
        attribute = attributes[index]
        if attribute['name'] not in ['slug', 'created', 'updated']:
            result_list.append(attribute)
            print('contain {}'.format(attribute['name']))

    result_dict['attributes'] = result_list
    return result_dict


def read_file(file_name):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name), "r") as f:
        template_string = ''
        for line in f.readlines():
            template_string += line
        f.close()
    return template_string


def read_json(src="project.json"):
    result = read_file(src)
    return jsonpickle.json.loads(result)


def read_file_model(json_path):
    json_object = read_json(json_path)
    return json_object


def read_template(template_name):
    model = read_file(os.path.join("resource", template_name))
    return model


def get_real_type(value: str):
    if value.lower() == 'false':
        return False
    elif value.lower() == 'true':
        return True
    elif re.match('^[0-9]*\.[0-9]*$', value):
        return float(value)
    elif re.match('^[0-9]*$', value):
        return int(value)
    else:
        return value


def generate_model_json_from_array(model_array) -> dict:
    model_dict = {}
    attribute_item = {}
    type_values = []
    attributes = []
    for item in model_array:
        clean_item = item.replace(' ', '')
        if 'class' in clean_item:
            model_dict['name'] = clean_item.replace('class', '')
        else:
            split_values = clean_item.split('=')
            if 'args=(self.slug,))' in clean_item:
                model_dict['identifier'] = 'slug'
            elif 'args=(self.pk,))' in clean_item:
                model_dict['identifier'] = 'pk'
            elif 'args=(self.id,))' in clean_item:
                model_dict['identifier'] = 'id'
            elif clean_item.endswith(',)') or clean_item.endswith(')'):
                pass
                type_values.append(
                    {
                        'name': split_values[0],
                        'value': get_real_type(split_values[1].replace(')', '').replace(',', ''))
                    }
                )
                attribute_item['type_value'] = type_values
                attributes.append(attribute_item)
                type_values = list()
                attribute_item = dict()
            elif clean_item.endswith(','):
                pass
                type_values.append(
                    {
                        'name': split_values[0],
                        'value': get_real_type(split_values[1].replace(')', '').replace(',', ''))
                    }
                )
            else:
                attribute_item['name'] = split_values[0]
                attribute_item['type'] = split_values[1]

    model_dict['attributes'] = attributes
    # print(jsonpickle.dumps(model_dict))
    return model_dict


def test_model_reader():
    django_directory = 'django-app'
    if os.path.isdir(django_directory):
        for (dirpath, dirnames, filenames) in os.walk(django_directory):
            list_dir = os.listdir(dirpath)
            for item_file in list_dir:
                path_file = dirpath + '/' + item_file
                if os.path.isfile(path_file) and 'models.py' in item_file:
                    result = read_file(path_file)
                    all_list = re.findall('class\s\w*|\w+\s*=\(*\s*\w*\.*\w+\,*\s*\)*', result)
                    model_data = generate_model_json_from_array(all_list)


def test_json_reader():
    django_directory = 'django-app'
    if os.path.isdir(django_directory):
        for (dirpath, dirnames, filenames) in os.walk(django_directory):
            list_dir = os.listdir(dirpath)
            for item_file in list_dir:
                path_file = dirpath + '/' + item_file
                if os.path.isfile(path_file) and '.json' in item_file:
                    result = read_file(path_file)
                    print(result)


#############################

def combine_json_template(json, template: str):
    jinja_template = Template(template)
    result_model = jinja_template.render(json)
    return result_model


def create_python_file(json, template):
    model_template = read_template(template)
    return combine_json_template(json, model_template)


def write_string(path, file_name, json):
    print(os.path.join(path, file_name))
    py_file = open(os.path.join(path, file_name), 'wt')
    py_file.write(json)
    py_file.close()


def write_model(parent_dir, json, ignore_file: list = list()):
    try:
        model_dir = os.path.join(parent_dir, json['name'].lower())
        migration_dir = os.path.join(model_dir, 'migrations')
        template_dir = os.path.join(model_dir, 'templates')
        model_template_dir = os.path.join(template_dir, json['name'].lower())

        pathlib.Path(model_dir).mkdir(parents=False, exist_ok=True)
        pathlib.Path(migration_dir).mkdir(parents=False, exist_ok=True)
        pathlib.Path(template_dir).mkdir(parents=False, exist_ok=True)
        pathlib.Path(model_template_dir).mkdir(parents=False, exist_ok=True)

        write_string(migration_dir, '__init__.py', '')
        write_string(model_dir, '__init__.py', '')
        print("-----------test-------------")

        model_clean_attribute = remove_read_only_attribute(json)

        for python_target_file in LIST_PYTHON_FILE:
            if python_target_file not in ignore_file:
                if python_target_file == 'forms':
                    combine_data = create_python_file(model_clean_attribute, python_target_file + ".tmp")
                else:
                    combine_data = create_python_file(json, python_target_file + ".tmp")
                write_string(model_dir, python_target_file + ".py", combine_data)

        models = create_python_file(json, 'html_menu.tmp')
        write_string(model_template_dir, 'menu.html', models)

        models = create_python_file(json, 'html_list_models.tmp')
        write_string(model_template_dir, '{}_list.html'.format(json['name'].lower()), models)

        models = create_python_file(json, 'html_form_models.tmp')
        write_string(model_template_dir, '{}_form.html'.format(json['name'].lower()), models)

        models = create_python_file(json, 'html_detail_models.tmp')
        write_string(model_template_dir, '{}_detail.html'.format(json['name'].lower()), models)

        models = create_python_file(json, 'html_delete_confirmation_models.tmp')
        write_string(model_template_dir, '{}_confirm_delete.html'.format(json['name'].lower()), models)
    except:
        print("exception")


def write_file(parent_dir=''):
    list_json = read_file_model()
    for json in list_json:
        write_model(parent_dir, json)


##############

def generate_from_model(app_path):
    path = pathlib.Path.cwd()
    # result_path = os.path.join(path, app_path)
    if os.path.isdir(app_path):
        for (dirpath, dirnames, filenames) in os.walk(app_path):

            list_dir = os.listdir(dirpath)

            for item_file in list_dir:

                path_file = dirpath + '/' + item_file

                if os.path.isfile(path_file) and 'models.py' in item_file:

                    result = read_file(path_file)

                    is_ignore = "DJENERATE-IGNORE" in result
                    print('data ignore {} {}'.format(is_ignore, path_file))
                    if not is_ignore:
                        result = result.replace('\'\'', 'None').replace('\'', '')
                        all_list = re.findall('class\s\w*|\w+\s*=\(*\s*\w*\.*\w+\,*\s*\)*', result)
                        model_data = generate_model_json_from_array(all_list)
                        model_data['identifier'] = {'name': 'pk', 'type': 'Int'}
                        for attribute in model_data['attributes']:
                            if 'slug' == attribute['name']:
                                model_data['identifier'] = {'name': 'slug', 'type': 'slug'}
                                break
                        write_model(app_path, model_data, ['models'])


def generate_from_json(app_path, ignored_list: list = list()):
    # path = pathlib.Path.cwd()
    # result_path = os.path.join(path, app_path)
    json_path = os.path.join(app_path, 'scheme')
    if os.path.isdir(json_path):
        for (dirpath, dirnames, filenames) in os.walk(json_path):
            list_dir = os.listdir(dirpath)
            for item_file in list_dir:
                path_file = dirpath + '/' + item_file
                if os.path.isfile(path_file) and '.json' in item_file:
                    result = read_file_model(path_file)
                    write_model(app_path, result)
    else:
        print("directory not exist")


def app(path, mode):
    if mode == 'json':
        generate_from_json(path)
    elif mode == 'model':
        generate_from_model(path)
    else:
        print('not support command')


if __name__ == '__main__':
    app('django-app', 'model')
    # result_path = os.path.join(path, 'django-app')
    # pathlib.Path(result_path).mkdir(parents=False, exist_ok=True)
    # write_file(result_path)
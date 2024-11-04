import json
import jsonschema, yaml


def main():
    with open('add_user.yml', 'r') as yml_file:
        new_user_conf = yaml.safe_load(yml_file)

    with open('add_user_schema.json') as schema_file:
        schema = json.load(schema_file)

    if jsonschema.validate(instance=new_user_conf, schema=schema) is None:
        print('Validation was completed successfully.')


if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Code Generator using Jinja2 Templates

使用 Jinja2 模板生成 FastAPI 代码文件。

Usage:
    python generate_code.py --parsed-data parsed.json --output-dir ./app --templates-dir ../assets/templates
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, List
from jinja2 import Environment, FileSystemLoader, Template


def map_openapi_type_to_python(openapi_type: str, format: str = None) -> str:
    """映射 OpenAPI 类型到 Python/Pydantic 类型"""
    type_mapping = {
        'string': 'str',
        'integer': 'int',
        'number': 'float',
        'boolean': 'bool',
        'array': 'List',
        'object': 'Dict[str, Any]',
    }

    if openapi_type == 'string' and format:
        format_mapping = {
            'date': 'date',
            'date-time': 'datetime',
            'email': 'EmailStr',
            'uri': 'AnyUrl',
            'uuid': 'UUID4',
            'password': 'SecretStr',
        }
        return format_mapping.get(format, 'str')

    return type_mapping.get(openapi_type, 'Any')


def map_openapi_type_to_sqlalchemy(openapi_type: str, format: str = None, max_length: int = None) -> str:
    """映射 OpenAPI 类型到 SQLAlchemy 类型"""
    if openapi_type == 'string':
        if format == 'date':
            return 'Date'
        elif format == 'date-time':
            return 'DateTime'
        elif format == 'uuid':
            return 'String(36)'
        elif max_length:
            return f'String({max_length})'
        else:
            return 'String'
    elif openapi_type == 'integer':
        if format == 'int64':
            return 'BigInteger'
        return 'Integer'
    elif openapi_type == 'number':
        if format == 'double':
            return 'Double'
        return 'Float'
    elif openapi_type == 'boolean':
        return 'Boolean'
    elif openapi_type == 'array':
        return 'JSON'  # SQLite doesn't have native array type
    elif openapi_type == 'object':
        return 'JSON'
    else:
        return 'String'


def prepare_model_context(schema_name: str, schema_def: Dict[str, Any]) -> Dict[str, Any]:
    """准备 model 模板的上下文数据"""
    fields = []

    for prop in schema_def.get('properties', []):
        field = {
            'name': prop['name'],
            'type': map_openapi_type_to_sqlalchemy(
                prop['type'],
                prop.get('format'),
                prop.get('maxLength')
            ),
            'nullable': prop['name'] not in schema_def.get('required', []),
            'unique': prop.get('format') == 'email',  # email 字段通常 unique
            'index': prop.get('format') == 'email',   # email 字段需要索引
            'default': prop.get('default'),
        }
        fields.append(field)

    # 提取 enums
    enums = []
    for enum_def in schema_def.get('enums', []):
        enums.append({
            'name': enum_def['name'],
            'values': enum_def['values']
        })

    context = {
        'model_name': schema_name,
        'table_name': schema_name.lower() + 's',  # 简单复数化
        'description': schema_def.get('description', f'{schema_name} model'),
        'fields': fields,
        'enums': enums,
        'has_enum': len(enums) > 0,
        'has_foreign_key': False,  # TODO: 检测外键
        'has_relationship': False,  # TODO: 检测关系
        'has_timestamps': True,  # 默认添加时间戳
        'relationships': [],
    }

    return context


def prepare_schema_context(schema_name: str, schema_def: Dict[str, Any]) -> Dict[str, Any]:
    """准备 schema 模板的上下文数据"""
    base_fields = []
    required_create_fields = []
    update_fields = []

    for prop in schema_def.get('properties', []):
        python_type = map_openapi_type_to_python(prop['type'], prop.get('format'))

        # 检查是否需要特殊导入
        has_email = python_type == 'EmailStr'
        has_url = python_type == 'AnyUrl'
        has_uuid = python_type == 'UUID4'

        is_required = prop['name'] in schema_def.get('required', [])

        field_config = []
        if prop.get('minLength'):
            field_config.append(f"min_length={prop['minLength']}")
        if prop.get('maxLength'):
            field_config.append(f"max_length={prop['maxLength']}")
        if prop.get('minimum') is not None:
            field_config.append(f"ge={prop['minimum']}")
        if prop.get('maximum') is not None:
            field_config.append(f"le={prop['maximum']}")

        field = {
            'name': prop['name'],
            'type': python_type,
            'optional': not is_required,
            'field_config': ', '.join(field_config) if field_config else None,
        }

        base_fields.append(field)

        if is_required:
            required_create_fields.append(field)

        update_fields.append(field)

    # 提取 enums
    enums = []
    for enum_def in schema_def.get('enums', []):
        enums.append({
            'name': enum_def['name'],
            'values': enum_def['values'],
            'description': f'{enum_def["name"]} enum'
        })

    context = {
        'model_name': schema_name,
        'base_fields': base_fields,
        'required_create_fields': required_create_fields,
        'update_fields': update_fields,
        'enums': enums,
        'has_email': any(f['type'] == 'EmailStr' for f in base_fields),
        'has_url': any(f['type'] == 'AnyUrl' for f in base_fields),
        'has_uuid': any(f['type'] == 'UUID4' for f in base_fields),
        'has_field_validator': any(f.get('field_config') for f in base_fields),
        'has_date': any(f['type'] == 'date' for f in base_fields),
        'has_list': any('List' in f['type'] for f in base_fields),
        'has_timestamps': True,
        'has_updated_at': True,
    }

    return context


def prepare_router_context(resource: str, endpoints: List[Dict[str, Any]]) -> Dict[str, Any]:
    """准备 router 模板的上下文数据"""
    processed_endpoints = []

    for endpoint in endpoints:
        # 提取路径参数
        path_params = [
            {'name': p['name'], 'type': map_openapi_type_to_python(p['type'])}
            for p in endpoint['parameters']['path']
        ]

        # 提取查询参数
        query_params = [
            {
                'name': p['name'],
                'type': map_openapi_type_to_python(p['type']),
                'default': p.get('default', '0' if p['type'] == 'integer' else '""'),
                'ge': p.get('minimum'),
                'le': p.get('maximum'),
            }
            for p in endpoint['parameters']['query']
        ]

        # 请求体
        request_body = None
        if endpoint.get('requestBody'):
            request_body = {
                'name': f"{resource}_in",
                'type': endpoint['requestBody'].get('schema_name', f"{resource.capitalize()}Create"),
            }

        # 响应模型
        response_200 = endpoint['responses'].get('200', {})
        response_model = response_200.get('schema_name') if response_200 else None

        # 生成函数名
        function_name = endpoint['operationId'].replace('-', '_').replace(' ', '_').lower()

        processed_endpoints.append({
            'method': endpoint['method'],
            'path': endpoint['path'],
            'function_name': function_name,
            'description': endpoint.get('description') or endpoint.get('summary', ''),
            'summary': endpoint.get('summary', ''),
            'path_params': path_params,
            'query_params': query_params,
            'request_body': request_body,
            'response_model': f"schemas.{response_model}" if response_model else None,
            'status_code': 'HTTP_201_CREATED' if endpoint['method'] == 'post' else None,
            'return_type': response_model or 'Any',
            'tags': endpoint.get('tags', []),
        })

    context = {
        'resource_name': resource,
        'endpoints': processed_endpoints,
        'crud_name': resource.lower(),
        'has_query_params': any(e['query_params'] for e in processed_endpoints),
        'has_optional': True,
    }

    return context


def generate_files(parsed_data_file: str, output_dir: str, templates_dir: str):
    """生成所有代码文件"""
    # 加载解析后的数据
    parsed = json.loads(Path(parsed_data_file).read_text())

    # 设置 Jinja2 环境
    env = Environment(loader=FileSystemLoader(templates_dir))

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 生成 models
    models_dir = output_path / 'models'
    models_dir.mkdir(exist_ok=True)

    for schema_name, schema_def in parsed['schemas'].items():
        context = prepare_model_context(schema_name, schema_def)
        template = env.get_template('model.py.j2')
        content = template.render(**context)

        model_file = models_dir / f"{schema_name.lower()}.py"
        model_file.write_text(content)
        print(f"✅ Generated: {model_file}")

    # 生成 schemas
    schemas_dir = output_path / 'schemas'
    schemas_dir.mkdir(exist_ok=True)

    for schema_name, schema_def in parsed['schemas'].items():
        context = prepare_schema_context(schema_name, schema_def)
        template = env.get_template('schema.py.j2')
        content = template.render(**context)

        schema_file = schemas_dir / f"{schema_name.lower()}.py"
        schema_file.write_text(content)
        print(f"✅ Generated: {schema_file}")

    # 生成 routers
    routers_dir = output_path / 'routers'
    routers_dir.mkdir(exist_ok=True)

    for resource, endpoints in parsed['paths'].items():
        context = prepare_router_context(resource, endpoints)
        template = env.get_template('router.py.j2')
        content = template.render(**context)

        router_file = routers_dir / f"{resource}.py"
        router_file.write_text(content)
        print(f"✅ Generated: {router_file}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Generate FastAPI code from parsed OpenAPI data')
    parser.add_argument('--parsed-data', required=True, help='Path to parsed OpenAPI JSON file')
    parser.add_argument('--output-dir', required=True, help='Output directory for generated code')
    parser.add_argument('--templates-dir', required=True, help='Directory containing Jinja2 templates')

    args = parser.parse_args()

    try:
        generate_files(args.parsed_data, args.output_dir, args.templates_dir)
        print("\n✅ Code generation complete!")
    except Exception as e:
        print(f"\n❌ Error generating code: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

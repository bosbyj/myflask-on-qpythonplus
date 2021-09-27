import os

import pytest
from pydantic.error_wrappers import ValidationError

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


def test_db_file():
    """测试是否存在数据库文件."""
    assert os.path.isfile('tmdata.db')


def test_index(client):
    """访问首页404."""
    rv = client.get('/')
    assert b'Not Found' in rv.data


def test_api_without_params(client):
    """零参数报错: 验证错误."""
    with pytest.raises(ValidationError):
        rv = client.get('/api/')


def test_api_with_param_keywords_equals_biancheng(client):
    # 如果是500k的大文件
    if os.stat('tmdata.db').st_size == 306085888:
        rv = client.get('/api/?keywords=编程')
        assert rv.status_code == 200
        assert rv.headers['Content-Type'] == "application/json"

        response_body = rv.json
        assert response_body['count'] == 7
        assert isinstance(response_body['duration'], float)
        assert response_body['page'] == 1
        assert response_body['total_pages'] == 1
        assert response_body['error'] is None
        assert response_body['results'][0]['rowid'] == 207927
        assert response_body['results'][0]['zh'] == '计算机编程'
        assert response_body['results'][0]['es'] == 'Programación informática'
    else:
        pass


def test_api_with_param_keywords_equals_programacion(client):
    # 如果是500k的大文件
    if os.stat('tmdata.db').st_size == 306085888:
        rv = client.get('/api/?keywords=programacion&language=es')
        assert rv.status_code == 200
        assert rv.headers['Content-Type'] == "application/json"

        response_body = rv.json
        assert response_body['count'] == 500
        assert isinstance(response_body['duration'], float)
        assert response_body['page'] == 1
        assert response_body['total_pages'] == 10
        assert response_body['error'] is None
        assert response_body['results'][0]['rowid'] == 207927
        assert response_body['results'][0]['zh'] == '计算机编程'
        assert response_body['results'][0]['es'] == 'Programación informática'
    else:
        pass


def test_api_with_param_keywords_equals_open_parenthesis(client):
    rv = client.get('/api/?keywords=(')
    assert rv.status_code == 200
    assert rv.headers['Content-Type'] == "application/json"

    response_body = rv.json
    assert 'fts5: syntax error' in response_body['error']

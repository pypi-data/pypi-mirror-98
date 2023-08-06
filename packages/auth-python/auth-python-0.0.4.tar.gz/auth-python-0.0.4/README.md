# auth-python

SaaS权限校验python sdk

- 升级安装必要工具

```python
python3 -m pip install --upgrade build
python3 -m pip install --user --upgrade twine
```

- 生成安装包

```python
python3 -m build
```

- 上传安装包

```python
python3 -m twine upload --repository-url https://<私有镜像地址> dist/*
```

默认上传到 https://pypi.org

```python
python3 -m twine upload  dist/*
```

### 使用安装包

- install

```python
pip3 install auth-python
```

### 使用

参考./test/auth_test.py
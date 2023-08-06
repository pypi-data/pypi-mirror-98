# flask_httpclient帮助文档

## 简介

对 requests 库进行包装，需要在 Flask 配置文件或对象创建时配置以下参数：
* 请求URL： {config_prefix}_URL/base_url
* 请求超时：{config_prefix}_TIMEOUT/timeout
* 实例前缀：config_prefix
* 重试次数：retry


## 安装


```python
    pip install flask-httpclient
```

## 使用

```python
    from flask_httpclient import HTTPClient

    http_client = HTTPClient(base_url='xxx',timeout=1, config_prefix='OPEN_API')

    # 创建 Flask 应用时集成扩展
    def create_app():
        app = Flask(__name__)
        http_client.init_app(app)
    
    # app 中使用
    resp = http_client.get('/users', params=params)
```

## License

[MIT](https://github.com/pythonml/douyin_image/blob/master/LICENSE)
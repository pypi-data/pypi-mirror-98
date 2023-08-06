# 企业微信接口

### 项目介绍
封装企业微信接口,发送消息.


### 安装教程
上传
```bash
export VERSION=0.0.2.3
python setup.py sdist && twine upload -u haifengat dist/*$VERSION*.gz && \
python setup.py bdist_wheel && twine upload -u haifengat dist/*$VERSION*.whl
```

` pip install work_weixin `

### 使用说明

#### launch.json
```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "main.py",
            "cwd": "${workspaceFolder}",
            "env": {
                "corpid": "wxxxxxxxxxxxxxxxxxxx",
                "agentid": "nnnnnnnn",
                "secret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
            },
            "console": "integratedTerminal"
        }
    ]
}
```

# 角色权限

角色权限采用可视化操作，对django进行了重构。

# 同步权限和菜单

## 手动同步

在第一次运行的时候 和增加model、admin之后，需要进行同步

```python
python3 manage.py syncmenu
```

## 自动同步




## 用户模型

simplepro中重构了角色权限相关，所以不能直接继承`AbstractUser`达到重写UserModel的目的。

需要继承simplepro的`AbstractExtendUser`来重写用户模型。

然后在settings.py正常配置即可。

```python
SIMPLEPRO_AUTH_USER_MODEL='你的模型'
```
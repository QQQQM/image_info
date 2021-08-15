# 使用方法
```python
python main.py image_name(=busybox) [select_num = 0]
```
## select_num = 0 (默认为此方式)
获取各layer id并保存为"Layer_$image_name.txt"格式
## select_num = 1
获取镜像的history信息并保存为"History_$image_name.json"格式
## select_num = 2
获取镜像的inspect信息并保存为"Inspect_$image_name.json"格式

### * 如果不存在本地镜像将会自动拉取对应的镜像 
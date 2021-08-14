# 使用方法
```python
python main.py image_name(=busybox) [select_num = 0]
```
## select_num = 0
获取各layer id并保存为"Layer_$image_name.txt"格式
## select_num = 1
获取镜像的history信息并保存为"History_$image_name.json"格式
## select_num = 2
获取镜像的inspect信息并保存为"Inspect_$image_name.json"格式
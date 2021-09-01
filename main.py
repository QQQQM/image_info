import os
import sys
import json
import docker
import pymysql
from docker.models.images import Image

def test1():
    print("hello")
    client = docker.APIClient(base_url='unix://var/run/docker.sock')
    dic = client.inspect_config("453d5e85856052a33f25954ea491648d4f465b073a0b13257734271534ce25ee")
    print(dic)


def read_json(filename, cur ):
    with open(filename,'r',encoding='utf8')as fp:
        json_data = json.load(fp)
        for i in range(len(json_data)):
            sql = "insert into image_id_list(name) values(\"" + json_data[i]["name"] + "\");"
            cur.execute(sql)

def collect_info(pathname):
    conn = pymysql.connect(
            host = 'localhost',#mysql服务器地址
            port = 3306,#端口号
            user = "root",
            passwd = "123456",
            db = 'test',#数据库名称
        )
    cur = conn.cursor()#创建并返回游标

    file_list = os.listdir(pathname)
    for file in file_list:
        file_name_full = pathname + "/" + file
        print(file_name_full)
        read_json(file_name_full, cur )
    
    conn.commit()
    cur.close()   
    conn.close()#关闭对象

def test(name_root):
    list_tem = []
    list_notall = []
    sava_place = "./data/" + name_root + ".json"
    notlist_filename = "./not_list/" + name_root + "_notlist.json"
    
    client = docker.from_env()
    for i1 in range(97,123):
        print(chr(i1))
        for i2 in range(97,123):
            search_name = name_root + chr(i1) + chr(i2)
            data = client.api.search(search_name,limit=100)
            if len(data) == 100:
                list_notall.append(search_name)
            list_tem += data
    save_jsonfile (sava_place, list_tem)
    save_jsonfile (notlist_filename, list_notall)


def save_jsonfile(filename,data):
    with open(filename,"w") as file_obj:
        json.dump(data,file_obj,sort_keys=True,indent=2)
    file_obj.close()
    # print_in_json(data)
    print("done!")

def print_in_json (data):
    json_str = json.dumps(data, sort_keys=True, indent=2)
    print(json_str)


def pull_image(image_name,client):
    print("pulling...")
    try:
        client.images.pull(image_name, tag=None,all_tags=False)
    except docker.errors.APIError as err:
        print(err)
        return err
    print(image_name, "pulled!")
    return None

def test_if_exist(image_name):
    print("dealing with :", image_name)
    client = docker.from_env()
    try:
        data = client.images.get(image_name)
        print(data)
        print(type(data))
        print(data.tags)
        image_name = data.tags[0]

    except docker.errors.ImageNotFound as e:
        print("可能本地不存在", image_name, "镜像，出现 error:", e , "\n")
        err = pull_image(image_name,client)
        if err != None:
            return err
        return None
    return None


def get_detail(image_name,function,type_name):
    print("Getting", type_name, "information...")
    filename = type_name + image_name + ".json"
    data = function(image_name)
    with open(filename,"w") as file_obj:
        json.dump(data,file_obj,sort_keys=True,indent=2)
    file_obj.close()
    # print_in_json(data)
    print("done!")


def get_imageid(image_name):
    print("Getting layer information...")
    layer_filename = "Layer_" + image_name + ".txt"
    layer_file = open(layer_filename,"w")

    client = docker.from_env()
    data = client.api.inspect_image(image_name)

    layer_file.write("Image Name:" + image_name + "\n")
    for cnt, i in enumerate(data["RootFS"]["Layers"]):
        layer_file.write("Layer" + str(cnt) + ":" + i + "\n")
    layer_file.write("Image Id:" + data["Id"])
    layer_file.close() 
    print("Done!")

def main():
    # for j in range(ord("c"),123):
    #     for i in range(97,123):
    #         test("a" + chr(j)+ chr(i))
    # return

    image_name = "busybox" if len(sys.argv)  == 1 else sys.argv[1]
    select = int(sys.argv[2]) if len(sys.argv)  == 3 else 0
    client = docker.from_env()
    err = test_if_exist(image_name)
    if err != None:
        return
    
    if select == 0:
        get_imageid(image_name)
    elif select == 1:
        get_detail(image_name, client.api.history, "History_")
    elif select ==2:
        get_detail(image_name, client.api.inspect_image, "Inspect_")
    elif select == 3:
        # path = os.getcwd()
        collect_info("./data/")
    elif select == 4:
        test1()
    else:
        pass

if __name__ == "__main__":
    main()

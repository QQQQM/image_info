import sys
import json
import docker
from docker.models.images import Image

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
    else:
        pass

if __name__ == "__main__":
    global image_name
    main()

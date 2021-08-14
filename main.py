import sys
import json
import docker

def pull_image(image_name):
    print("hello")

def test(image_name):
    print(image_name)
    client = docker.from_env()
    
    try:
        print(client.images.list(all = True))
    except docker.errors.ImageNotFound as e:
        print("error:",e)
        pull_image(image_name)
    finally:
        print("end")



def get_detail(image_name,function,type_name):
    filename = type_name + image_name + ".json"
    data = function(image_name)
    json_str = json.dumps(data, sort_keys=True, indent=2)
    print(json_str)
    with open(filename,"w") as file_obj:
        json.dump(data,file_obj,sort_keys=True,indent=2)
    file_obj.close()


def get_imageid(image_name):
    layer_filename = "Layer_" + image_name + ".txt"
    layer_file = open(layer_filename,"w")

    client = docker.from_env()
    data = client.api.inspect_image(image_name)

    layer_file.write("Image Name:" + image_name + "\n")
    for cnt, i in enumerate(data["RootFS"]["Layers"]):
        layer_file.write("Layer" + str(cnt) + ":" + i + "\n")
    layer_file.write("Image Id:" + data["Id"])
    layer_file.close()

def main():
    image_name = "busybox" if len(sys.argv)  == 1 else sys.argv[1]
    select = int(sys.argv[2]) if len(sys.argv)  == 3 else 0
    client = docker.from_env()
    
    if select == 0:
        get_imageid(image_name)
    elif select == 1:
        get_detail(image_name, client.api.history, "History_")
    elif select ==2:
        get_detail(image_name, client.api.inspect_image, "Inspect_")
    else:
        test(image_name)

if __name__ == "__main__":

    main()

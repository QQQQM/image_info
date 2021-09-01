# coding:utf-8
import csv
import re
from textblob import TextBlob


def write_file(filename,list):
    csv_writer = csv.writer(filename)
    csv_writer.writerow(list)

def analyse(text):
    blob = TextBlob(text)
    sub = 0
    sub2 = 0
    for sentence in blob.sentences:
        sub += sentence.sentiment.polarity
        sub2 += sentence.sentiment.subjectivity
        write_file(save_file, ["", "", "", "", "", "", "", "", "","", sentence, str(sentence.sentiment.polarity),str(sentence.sentiment.subjectivity)])
    write_file(save_file, [sub, sub2,str(blob.polarity),str(blob.subjectivity)])

def read(csv_file, save_file):
    reader = csv.reader(csv_file)
    flag = True
    for row in reader:
        write_file(save_file, [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]])
        if flag:
            flag = False
            continue        
        analyse(row[9])


if __name__ == "__main__":
    str = "hell\\\"o"
    print(str)
    k = re.sub("\\\\\"","\"",str)
    print(k)
    
    # save_file = open('情感分析.csv','w',encoding='utf-8')
    # csv_file = open("./yv.csv", encoding='utf-8')
    # read(csv_file, save_file)
    # save_file.close()


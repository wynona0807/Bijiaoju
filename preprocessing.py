# -*- coding:utf-8 -*-
import os 
import jieba
import pymongo
import jieba.posseg as pseg


def getID(initline):
	pos1 = initline.index("<")
	pos2 = initline.index(">")
	idstr = initline[pos1+1:pos2]

	return idstr;


def testMethod():
	meragefiledir = os.getcwd()+'\\cars'
	filenames=os.listdir(meragefiledir) 
	# print(meragefiledir)


	classname=""
	tpyename=""
	# print(filenames)
	for filename in filenames:

		data = open("cars/"+filename,"r",encoding="UTF-8")

		for line in data:
			print(line)
			idstr = getID(line)
			print(idstr)

def dataProcess(filename,tpyename,classname,testAnswer, collection):
	data = open("cars/"+filename,"r",encoding="UTF-8")
	# print(data)
	
	Id=""
	sentence=""

	for line in data:
		# print(line)
		index = line.index(">")
		Id =getID(line)
		# print(Id)
		sentence = line[index+1:line.index("</")]
		# print(sentence)

		segline = segment(sentence)
		segtag = segmentwithtag(sentence)
		# print(segline)
		
		#定义字典
		dic={}
		if( Id in testAnswer):
			dic={"Id":Id,"sentence":sentence,"tpyename":tpyename,"classname":classname,"segment":segline,"segmentwithtag":segtag,"answer":testAnswer[Id]}
		else:
			dic={"Id":Id,"sentence":sentence,"tpyename":tpyename,"classname":classname,"segment":segline,"segmentwithtag":segtag,"answer":-1}
		print(dic)
		
		collection.insert_one(dic)




def segment(line):#分词

	words=" ".join(jieba.cut(line,cut_all=False))
	# print(words)
			# seg_list.append(words)
			# # print(seg_list)	

	return words

def segmentwithtag(line):#词性标注

	words=pseg.cut(line)
	result=[]
	
	for word, flag in words:
		result.append(word + "/"+flag)
		words=" ".join(result)
	# print(words)

	return words			

	


 


def process():
	myclient=pymongo.MongoClient("mongodb://localhost:27017/")
	mydb=myclient["ComparativeSentenceCorpus"]
	collection = mydb["digitalCar"]
	meragefiledir = os.getcwd()+'\\cars'
	filenames=os.listdir(meragefiledir) 
	# print(meragefiledir)
	testAnswer = select()

	classname=""
	tpyename=""
	# print(filenames)
	for filename in filenames:
		# print(filename)
		if ("电子" in filename):
			classname="digital"
			
		
			if("测试" in filename):
				 
				tpyename="test"
			else:
				
				tpyename="train"
		else:
			classname="car"
			if ("测试" in filename):
				tpyename="test"
			else:
				tpyename="train"
		dataProcess(filename, tpyename,classname,testAnswer,collection)


def select():
	# myclient=pymongo.MongoClient("mongodb://localhost:27017/")
	# mydb=myclient["Corpus"]
	meragefiledir1= os.getcwd()+'\\answers'
	print(meragefiledir1)
	filenames=os.listdir(meragefiledir1)
	# print(filenames)
	docid=""#doc1234
	answer=""
	testAnswer ={}

	for filename in filenames:

		get_answer= open("answers/"+filename,"r",encoding="UTF-8")
		# print(get_answer)

		for line in get_answer:

			items = line.split("\t")
			# print(line)
			
			docid=items[1]

			# print(docid)
			
			# elements=line.split("/t")
			answer=int(items[3])
			# print(answer)
			testAnswer[docid]=answer

			#dataProcess(Id1,answer)

	# print(classname )
	# filename.index("电子")
	# filename.index("测试")
	# 判断好一个文件后打开并处理该文件
# def select():
	# print(testAnswer)
	return testAnswer
			# print(feature)
		# dataProcess(Id1,feature)





if __name__ == '__main__':
	process()
	# testMethod()
	# select()

	
	
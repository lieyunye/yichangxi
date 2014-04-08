from django.http import HttpResponse
import pylibmc
import pymongo

def testMemcache(request):
	mc = pylibmc.Client(["127.0.0.1:12000"], binary=True,
                     behaviors={"tcp_nodelay": True,
                                "ketama": True})
	print mc.isConnected()
	print "ssss"
	dic = {}
	dic['key1'] = "value1"
	dic['key2'] = "value2"

	mc.set("foo",dic)
	value = mc.get("foo")
	print value
	return HttpResponse("Ok")

def testMongoDB(request):
	conn = pymongo.Connection()
	db = conn.mydb
	testData = db.testData

	print testData.find_one({"x":4})
	return HttpResponse("Ok")
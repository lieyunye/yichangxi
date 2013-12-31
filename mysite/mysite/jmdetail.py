from django.http import HttpResponse
import pylibmc

def testMemcache(request):
	mc = pylibmc.Client(["127.0.0.1:12000"], binary=True,
                     behaviors={"tcp_nodelay": True,
                                "ketama": True})
	print mc
	dic = {}
	dic['key1'] = "value1"
	dic['key2'] = "value2"

	mc.set("foo",dic)
	value = mc.get("foo")
	print value
	return HttpResponse("Ok")
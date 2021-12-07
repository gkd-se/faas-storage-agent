from faassa import api
import random
import time

def handle(req):
    a = api.Agent()
    ns_name = "test_ns"
    repeat_counter = 2
    test_count = 11*repeat_counter
    count_ok = test_count
    time_start = time.time()

    for temp_i in range(repeat_counter):
        rand = str(random.randint(1,1000))
        key = "test_key_" + rand
        value = ("test_value" + rand).encode()
        
        c, i = a.create_ns(ns_name)
        if c != 0:
            count_ok -= 1
            print("create_ns test ... failed. err_info:", i)
        else:
            print("create_ns test ... ok")
        
        c, i = a.connect_ns(ns_name)
        if c != 0:
            count_ok -= 1
            print("connect_ns test ... failed. err_info:", i)
        else:
            print("connect_ns test ... ok")

        c, i = a.set(key, value)
        if c != 0:
            count_ok -= 1
            print("set test ... failed. err_info:", i)
        else:
            print("set test ... ok")

        c, i = a.exists(key)
        if c != 0:
            count_ok -= 1
            print("exists test ... failed. err_info:", i)
        else:
            print("exists test ... ok")

        c, i, v = a.get(key)
        if c != 0:
            print("get test ... failed. err_info:", i)
        elif v != value:
            count_ok -= 1
            print("get test ... failed. err value : ", v.decode())
        else:
            print("get test ... ok")

        c, i = a.delete(key)
        if c != 0:
            count_ok -= 1
            print("delete test ... failed. err_info:", i)
        else:
            print("delete test ... ok")
            
        c, i = a.exists(key)
        if c == 0:
            count_ok -= 1
            print("exists test ... failed. err_info:", i)
        else:
            print("exists test ... ok")

        c, i, v = a.get(key)
        if c == 0:
            count_ok -= 1
            print("get test ... failed. err_info:", i)
        else:
            print("get test ... ok")

        c, i = a.delete_ns(ns_name)
        if c != 0:
            count_ok -= 1
            print("delete_ns test ... failed. err_info:", i)
        else:
            print("delete_ns test ... ok")

        c, i = a.connect_ns(ns_name)
        if c == 0:
            count_ok -= 1
            print("connect_ns test ... failed. err_info:", i)
        else:
            print("connect_ns test ... ok")
        
        c, i = a.delete_ns(ns_name)
        if c == 0:
            count_ok -= 1
            print("delete_ns test ... failed. err_info:", i)
        else:
            print("delete_ns test ... ok")

    if count_ok == test_count :
        res = "ok"
    else :
        res = "failed"
    time_end = time.time()
    print("pressure test time: {} seconds; ".format(time_end - time_start))
    print("test result: {0}. {1} passed; {2} failed".format(res, count_ok, test_count - count_ok))
    return req

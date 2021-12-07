from faassa import api
import random
import time

def handle(req):
    repeat_counter = 3
    data_size = 100
    
    a = api.Agent()
    ns_name = "test_ns"
    # test_count = 11 * repeat_counter
    # count_ok = test_count
    # task_ok = [repeat_counter] * 11
    key = ["key"+str(random.randint(1,data_size)) for i in range(data_size)]
    value = [("val"+str(random.randint(1,data_size))).encode() for i in range(data_size)]
    key_exist = random.shuffle(["key" + str(i) for i in range(data_size)])
    key_delete = random.shuffle(list(set(key)))
    time_set = [0] * repeat_counter
    time_exists = [0] * repeat_counter
    time_get = [0] * repeat_counter
    time_delete = [0] * repeat_counter
    time_all_start = time.time()
    
    c, i = a.create_ns(ns_name)
    c, i = a.connect_ns(ns_name)

    for temp_i in range(repeat_counter):
        
        time_temp_start = time.time()
        for temp_j in range(data_size):
            c, i = a.set(key[temp_j], value[temp_j])
        time_temp_end = time.time()
        time_set[temp_i] = time_temp_end - time_temp_start

        time_temp_start = time.time()
        for ke in key_exist:
            c, i = a.exists(ke)
        time_temp_end = time.time()
        time_exists[temp_i] = time_temp_end - time_temp_start

        time_temp_start = time.time()
        for ke in key_exist:
            c, i = a.get(ke)
        time_temp_end = time.time()
        time_get[temp_i] = time_temp_end - time_temp_start
        
        time_temp_start = time.time()
        for kd in key_delete:
            c, i = a.delete(kd)
        time_temp_end = time.time()
        time_delete[temp_i] = time_temp_end - time_temp_start

    c, i = a.delete_ns(ns_name)

    time_all_end = time.time()
    # if count_ok == test_count :
        # res = "ok"
    # else :
        # res = "failed"
        # print(task_ok)
    print("pressure test time: {} seconds; ".format(time_all_end - time_all_start))
    print("set: {}".format(time_set))
    print("exists: {}".format(time_exists))
    print("get: {}".format(time_get))
    print("delete: {}".format(time_delete))
    
    # print("test result: {0}. {1} passed; {2} failed".format(res, count_ok, test_count - count_ok))
    return req

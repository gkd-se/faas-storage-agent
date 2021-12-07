from faassa import api
import random
import time

def handle(req):
    repeat_counter = 10
    
    a = api.Agent()
    ns_name = "test_ns"
    test_count = 11*repeat_counter
    count_ok = test_count
    time_start = time.time()
    task_ok = [repeat_counter] * 11

    for temp_i in range(repeat_counter):
        rand = str(random.randint(1,1000))
        key = "test_key_" + rand
        value = ("test_value" + rand).encode()
        
        c, i = a.create_ns(ns_name)
        if c != 0:
            count_ok -= 1
            task_ok[0] = task_ok[0] - 1
        
        c, i = a.connect_ns(ns_name)
        if c != 0:
            count_ok -= 1
            task_ok[1] = task_ok[1] - 1

        c, i = a.set(key, value)
        if c != 0:
            count_ok -= 1
            task_ok[2] = task_ok[2] - 1

        c, i = a.exists(key)
        if c != 0:
            count_ok -= 1
            task_ok[3] = task_ok[3] - 1

        c, i, v = a.get(key)
        if c != 0:
            count_ok -= 1
            task_ok[4] = task_ok[4] - 1
        elif v != value:
            count_ok -= 1
            task_ok[4] = task_ok[4] - 1

        c, i = a.delete(key)
        if c != 0:
            count_ok -= 1
            task_ok[5] = task_ok[5] - 1
            
        c, i = a.exists(key)
        if c == 0:
            count_ok -= 1
            task_ok[6] = task_ok[6] - 1

        c, i, v = a.get(key)
        if c == 0:
            count_ok -= 1
            task_ok[7] = task_ok[7] - 1

        c, i = a.delete_ns(ns_name)
        if c != 0:
            count_ok -= 1
            task_ok[8] = task_ok[8] - 1

        c, i = a.connect_ns(ns_name)
        if c == 0:
            count_ok -= 1
            task_ok[9] = task_ok[9] - 1
        
        c, i = a.delete_ns(ns_name)
        if c == 0:
            count_ok -= 1
            task_ok[10] = task_ok[10] - 1

    if count_ok == test_count :
        res = "ok"
    else :
        res = "failed"
        print(task_ok)
    time_end = time.time()
    print("pressure test time: {} seconds; ".format(time_end - time_start))
    print("test result: {0}. {1} passed; {2} failed".format(res, count_ok, test_count - count_ok))
    return req

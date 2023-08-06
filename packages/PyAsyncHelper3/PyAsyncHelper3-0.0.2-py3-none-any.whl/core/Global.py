
g_worker_dict = dict()


def set_worker(type,consumer):
    if type not in g_worker_dict.keys():
        g_worker_dict[type] = set()
    g_worker_dict[type].add(consumer)




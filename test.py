from message.send import Send
from message.send_debug import SendDebug
from message.receive import Receive

from thread_global.myRRTmerge import RRT as thread_RRT

from thread_local.xy_speed import XY_speed

from utils import select_info, distance, check_path_thread

import time, threading

global infos
global path, path_lines, tree, lines
global target_x, target_y
global x, y, ori
global vx, vy
global i
global color, id
global threshold
global status_coll, status


def receive_module():
    global infos
    global x, y, ori
    global i
    global color, id
    global threshold
    global vx, vy
    x , y = 0, 0
    vx = 0
    vy = 0
    threshold = 30
    i = 0
    infos = []
    receive = Receive()
    color = 'blue'
    id = 5
    while True:
        infos = receive.thread_infos()
        x, y, _, _, ori = select_info(infos, color, id)


def global_module():
    global infos
    global target_x
    global target_y
    global path, path_lines, tree, lines
    global x, y
    global i
    global status_coll, status
    path, path_lines, tree, lines = [], [], [], []
    target_x, target_y = 250, 180
    global_planner = thread_RRT
    status_coll = False
    status = False
    while not status_coll or not status:
        time_start = time.time()
        global_path = global_planner(x, y, target_x, target_y, infos, color=color, robot_id=id, inflateRadius=30)
        status, tree, lines = global_path.Generate_Path()
        path_, path_lines = global_path.Get_Path()
        print('ori:', len(path_))
        path, path_lines = global_path.merge()
        print('nodes:', len(path))
        time_end = time.time()
        print('path cost:', time_end - time_start)
        i = 0


def local_module():
    global x, y, ori
    global vx, vy
    global i
    global target_x, target_y
    global path
    global status_coll, status
    index = 1
    local_planner = XY_speed
    while True:
        if distance((x, y), (target_x, target_y)) > 30:
            N = len(path)
            if N < 1:
                continue
            try:
                motion = local_planner()
                vx, vy = motion.line_control(x, y, ori, path, i, N, info=infos, threshold=30)
                if i < N - 1:
                    status_coll, index = check_path_thread([x, y], path[i+1], infos, color=color, id=id,
                                          dis_threshold=threshold, index=index)
                if distance([x, y], path[i]) < 10:
                    i += 1
            except:
                vx, vy = 0, 0
                continue
        else:
            status = False
            target_x = -target_x
            target_y = -target_y


def send_module():
    while True:
        send = Send()
        send.send_msg(id, vx, vy, 0)
        print('vx', vx)
        print('vy', vy)


def debug_module():
    global lines, path_lines
    while True:
        debug_info = SendDebug('LINE', [lines, path_lines])
        debug_info.send()


if __name__ == '__main__':
    thread1 = threading.Thread(target=receive_module)
    thread2 = threading.Thread(target=global_module)
    thread3 = threading.Thread(target=local_module)
    thread4 = threading.Thread(target=send_module)
    thread5 = threading.Thread(target=debug_module)

    thread1.start()
    time.sleep(0.1)
    thread2.start()
    time.sleep(0.1)
    thread3.start()
    time.sleep(0.1)
    thread4.start()
    time.sleep(0.1)
    thread5.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()

import wxauto  # 修改1：切换到wxauto库
import os
import time
import threading  # 导入threading模块
import queue  # 导入queue模块
import ds


wxauto.SET_TIMEOUT = 15
wxauto.SET_SLEEP = 0.5

wx = wxauto.WeChat()
msg_list = []
friend_list = []
friend_path = 'friend.txt'
wait = 0.5  # 修改：减少监听间隔，提升消息响应速度
message_queue = queue.Queue()  # 创建队列用于线程间通信


def listen_new_msg():
    while True:
        try:
            new_msg = wx.GetNextNewMessage()
            for name in new_msg.keys():
                l = new_msg.get(name)
                for p in l:
                    if p.type == 'friend':
                        print(f"子线程监听到新消息: {p.content}")
                        message_queue.put({'name':p.sender_remark,'content':p.content})  # 放入队列
                    else:
                        continue
        except Exception as e:
            print(f"发生 COM 错误: {e}")
        time.sleep(wait)


if __name__ == '__main__':
    print("程序已启动，等待消息中...")

    # 启动子线程来监听新消息
    listen_thread = threading.Thread(target=listen_new_msg)
    listen_thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
    listen_thread.start()

    # 父线程从队列中获取消息字典并处理
    while True:
        new_msg = message_queue.get()  # 阻塞式获取消息，避免空循环
        print(f"父线程处理新消息: {new_msg.get('content')}")
        result = ds.get_response(new_msg.get('content'))
        wx.SendMsg(who=new_msg.get('name'), msg=result)
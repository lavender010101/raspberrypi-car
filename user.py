import cv2
import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_host = '172.22.10.233'
server_port = 2022  # 设置端口号
sock.connect((server_host, server_port))  # 连接服务，指定主机和端口

live_port = "8080"

if __name__ == "__main__":
    try:
        live_url = "http://" + server_host + ":" + live_port + "/?action=stream"
        cap = cv2.VideoCapture(live_url)
        cap.set(3, 640)
        cap.set(4, 480)  # 设置窗口的大小

        while True:
            ret, frame = cap.read()  # 将摄像头拍摄到的画面作为frame的值
            cv2.imshow('video', frame)  # 将具体的测试效果显示出来

            input_key = cv2.waitKey(5) & 0xFF
            if input_key == 27:  # 如果按了ESC就退出 当然也可以自己设置
                sock.sendall('exit'.encode('utf-8'))
                print('已经发送停止并且结束程序')
                break
            elif input_key == ord('w'):
                sock.sendall('forward'.encode('utf-8'))
            elif input_key == ord('s'):
                sock.sendall('backward'.encode('utf-8'))
            elif input_key == ord('a'):
                sock.sendall('turn_left'.encode('utf-8'))
            elif input_key == ord('d'):
                sock.sendall('turn_right'.encode('utf-8'))
            elif input_key == ord('h'):
                sock.sendall('servo_turn_left'.encode('utf-8'))
            elif input_key == ord('l'):
                sock.sendall('servo_turn_right'.encode('utf-8'))
            elif input_key == ord('j'):
                sock.sendall('servo_down'.encode('utf-8'))
            elif input_key == ord('k'):
                sock.sendall('servo_up'.encode('utf-8'))

    except KeyboardInterrupt:
        print('exit by Ctrl-C')

    finally:
        cap.release()
        cv2.destroyAllWindows()  # 后面两句是常规操作,每次使用摄像头都需要这样设置一波

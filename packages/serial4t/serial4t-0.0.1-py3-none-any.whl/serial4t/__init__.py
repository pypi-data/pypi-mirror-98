import serial
import serial.tools.list_ports
import os.path
import platform

__all__ = [ 
            '序列連接', '連接microbit'
            
            ]


## Custom Exceptions
class SecralConnectionError(Exception):
    def __init__(self, value):
        super().__init__(value)


def detect_potential_ports():
    # code from list_serial_ports 
    
    try:
        old_islink = os.path.islink
        if platform.system() == "Windows":
            os.path.islink = lambda _: False
        all_ports = list(serial.tools.list_ports.comports())
    finally:
        os.path.islink = old_islink

    return [(p.device, p.description) for p in all_ports 
                    if (p.vid, p.pid) in {(0x0D28, 0x0204)} ]






def 序列連接(埠, 傳輸率=115200, timeout=None):
    pass


def 連接microbit(埠='auto', 例外錯誤=True ,傳輸率=115200, 讀取等待=None):
    if 埠 == 'auto':
        #print('<< 自動偵測microbit.... >>')
        potential = detect_potential_ports()
        #print(potential)
        microbit_num = len(potential)
        if  microbit_num == 1:
            port = potential[0][0]
            print(f'<< 偵測到microbit, 在連接埠 {port} >> ' )
        elif microbit_num > 1:
            _, descriptions = zip(*potential)
            message = f'<< 偵測到{microbit_num}個microbit, 相關資訊如下 >>'
            message += "\n * " + "\n * ".join(descriptions)
            print(message)
            port = potential[0][0]
            print(f'<< 將使用連接埠({port}) >>')
        else :
            msg = '<< 偵測不到microbit, 請確認是否已接上電腦 >>'
            if 例外錯誤 :
                raise SecralConnectionError(msg)
            else:
                print(msg)
                return Connection(enable_exception=例外錯誤)

    else:
        port = 埠

    return Connection(port, 例外錯誤, 傳輸率, 讀取等待)


class Connection():
    def __init__(self, port=None, enable_exception=True, baudrate=115200, timeout=None):
        self.port = port
        self.enable_exception = enable_exception
        self.baudrate = baudrate
        self.timeout = timeout

        if port :
            # serial connect
            try:
                self.ser = serial.Serial(port, baudrate, timeout=timeout)
                note_text = port
                note_text += ' 有例外錯誤' if enable_exception else ' 無例外錯誤'
                note_text += ' 不等待' if timeout == 0 else ' 等待'
                print('<< microbit已連接 ({}) >>'.format(note_text))
            except serial.SerialException:
                msg = '<< 連接microbit時發生錯誤 >>'
                if self.enable_exception:
                    raise SecralConnectionError(msg)
                else:
                    print(msg)
        else:
            # no port
            self.ser = None

    def 傳送(self, send_bytes):
        if not self.ser:
            msg = '<< 沒有連接microbit >>'
            if self.enable_exception:
                raise SecralConnectionError(msg)
            else:
                print(msg)
                return

        try:
            if type(send_bytes) is not bytes:
                send_bytes = bytes(str(send_bytes), 'utf8')
            self.ser.write(send_bytes)

        except serial.SerialException:
            msg = '<< 傳送microbit時發生錯誤 >>'
            if self.enable_exception:
                raise SecralConnectionError(msg)
            else:
                print(msg)
                return       


    # def 傳送文字(self, send_text):
    #     if not self.ser:
    #         msg = '<< 沒有連接microbit >>'
    #         if self.enable_exception:
    #             raise SecralConnectionError(msg)
    #         else:
    #             print(msg)
    #             return

    def 接收(self, 位元組=0):
        # 位元組: 0或None讀取全部 ,  
        if not self.ser:
            msg = '<< 沒有連接microbit >>'
            if self.enable_exception:
                raise SecralConnectionError(msg)
            else:
                print(msg)
                return

        try:
            if self.timeout != 0:
                print('<< 等待讀取microbit... >>')

            if 位元組 > 0:
                return self.ser.read(size=位元組)
            else:
                # read all from input buffer
                data_num = self.ser.in_waiting
                #print('in_waiting: ', data_num)
                return self.ser.read(size=data_num)

        except serial.SerialException:
            msg = '<< 讀取microbit時發生錯誤 >>'
            if self.enable_exception:
                raise SecralConnectionError(msg)
            else:
                print(msg)
                return

    # def 接收文字(self):
    #     if not self.ser:
    #         msg = '<< 沒有連接microbit >>'
    #         if self.enable_exception:
    #             raise SecralConnectionError(msg)
    #         else:
    #             print(msg)
    #             return

    def 關閉(self):
        if not self.ser:
            msg = '<< 沒有連接microbit >>'
            if self.enable_exception:
                raise SecralConnectionError(msg)
            else:
                print(msg)
                return

        try:
            self.ser.close()
            print('<< 序列連線已關閉 >>')
            self.ser = None
        except serial.SerialException:
            msg = '<< 關閉microbit時發生錯誤 >>'
            if self.enable_exception:
                raise SecralConnectionError(msg)
            else:
                print(msg)
                return


    def 清除緩除區(self):
        if not self.ser:
            msg = '<< 沒有連接microbit >>'
            if self.enable_exception:
                raise SecralConnectionError(msg)
            else:
                print(msg)
                return

        try:
            self.ser.reset_input_buffer()        
        except serial.SerialException:
            msg = '<< 清除緩除區時發生錯誤 >>'
            if self.enable_exception:
                raise SecralConnectionError(msg)
            else:
                print(msg)
                return



### wrapper functions


if __name__ == '__main__' :
    pass
    

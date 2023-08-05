from flask import Flask
from flask_socketio import SocketIO
from flask import send_from_directory
from zumi.zumi import Zumi
from zumi.util.screen import Screen
from zumi.personality import Personality
from zumi.protocol import Note
import zumidashboard.scripts as scripts
import zumidashboard.sounds as sound
import zumidashboard.updater as updater
from zumidashboard.drive_mode import DriveMode
import time, subprocess, os, re, base64, cv2
from threading import Thread, Event
import threading
import ctypes
from subprocess import Popen
import logging, json
from logging.handlers import RotatingFileHandler
import code
import sys
from io import StringIO
import contextlib


if not os.path.isdir('/home/pi/Dashboard/debug'):
    os.mkdir('/home/pi/Dashboard/debug')

app = Flask(__name__, static_url_path="", static_folder='dashboard')
app.zumi = Zumi()
app.screen = Screen(clear=False)
app.personality = Personality(app.zumi, app.screen)
app.user = ''
app.language = 'en'
app.action = ''
app.action_payload = ''
app.wifi_list = set()
app.new_blockly_project = ''
socketio = SocketIO(app)
usr_dir = '/home/pi/Dashboard/user/'
handler = RotatingFileHandler('/home/pi/Dashboard/debug/dashboard.log', maxBytes=10000, backupCount=1)
app.logger.setLevel(logging.DEBUG)
app.logger.addHandler(handler)
lib_dir = os.path.dirname(os.path.abspath(__file__))
app.drive_mode = DriveMode(app.zumi)
app.copy_content = ''
app.knn = ''
app.camera = ''
app.wifi_msg = True
app.check_update_content = False
app.opening_streaming_server_proc = ''
app.update_user_content_thread = ''

app.run_code_process = ''
# manager = Manager()
# Global = manager.Namespace()
app.code_editor_locals = {}
app.run_code_value = ''
app.read_image = False
app.code_editor_globals = []
app.kill_run_code_thread = False
app.run_code_lock = ''

#refactoring--------
app.checked_internet = False
app.check_internet_thread = ''
app.internet_info = ''
app.need_to_update = False

app.connect_wifi_thread = ''
app.connected_wifi = False
#--------------/

# dashboard
vendor_static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard/blockly/src/app/vendor")
blockly_static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard/blockly/src/app/blockly-lib")
ui_library =  os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard/blockly/src/app/ble-lib")
blockly_fonts =  os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard/blockly/src/app/fonts")
blockly_images =  os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard/blockly/src/app/images")
blockly_media =  os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard/blockly/src/app/media")
blockly_msg =  os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard/blockly/src/app/msg")


# ------------------------------------------
#refactoring
class StoppableThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')
# ---------------------------------------------

def _awake():
    app.screen.hello()
    sound.wake_up_sound(app.zumi)


def log(msge):
    app.logger.info(time.strftime('{%Y-%m-%d %H:%M:%S} ')+msge)


@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# ide routes
@app.route('/zumi-code-editor')
def zumi_code_editor():
    return app.send_static_file('index.html')

@app.route('/zumi-code-editor-lesson')
def zumi_code_editor_lesson():
    return app.send_static_file('index.html')


# blockly ----------------------------------------------------------------------------------------------------
@app.route('/blockly')
def blockly():
    return app.send_static_file('./blockly/src/app/index.html')


@app.route('/vendor/<path:filename>')
def send_js(filename):
    return send_from_directory(vendor_static_dir, filename)


@app.route('/blockly-lib/<path:filename>')
def send_blocklydir(filename):
    return send_from_directory(blockly_static_dir, filename)


@app.route('/ble-lib/<path:filename>')
def send_ui_dir(filename):
    return send_from_directory(ui_library, filename)


@app.route('/fonts/<path:filename>')
def send_font_dir(filename):
    return send_from_directory(blockly_fonts, filename)


@app.route('/images/<path:filename>')
def send_images_dir(filename):
    return send_from_directory(blockly_images, filename)

@app.route('/media/<path:filename>')
def send_media_dir(filename):
    return send_from_directory(blockly_media, filename)

@app.route('/msg/<path:filename>')
def send_msg_dir(filename):
    return send_from_directory(blockly_msg, filename)


@socketio.on('clear_locals')
def clear_locals():
    app.code_editor_locals = {}
    app.code_editor_globals = []
    app.read_image = False


@socketio.on('run_code')
def run_code(source_code_base64):
    app.run_code_process = RunCodeThread(source_code_base64)
    app.run_code_process.start()


class RunCodeThread(Thread):
    """Thread class with a stop() method. The thread itself has to check
        regularly for the stopped() condition."""
    def __init__(self, source_code_base64):
        Thread.__init__(self)
        self.source_code_base64 = source_code_base64

    def run(self):
        read_variables(locals())

        source_code = base64.b64decode(self.source_code_base64).decode('utf-8')
        message = source_code.split("\n")

        library_lines = []
        image_variables = []

        with stdoutIO() as s:
            try:
                co = code.compile_command(source_code, "<stdin>", "exec")
                if co:
                    exec(co)
                for line in message:
                    if 'import' in line:
                        library_lines.append(line)
                    if '.capture(' in line:
                        variable = line.split("=")[0].replace(" ", "")
                        image_variables.append(variable)
                    if '.show_image(' in line:
                        key = line.split("(")[1].split(")")[0].replace(" ", "")
                        _frame = locals()[key]
                        _frame = cv2.cvtColor(_frame, cv2.COLOR_BGR2RGB)
                        cv2.imwrite(
                            '/usr/local/lib/python3.5/dist-packages/zumidashboard/dashboard/code_editor_image.jpg',
                            _frame)
                        app.read_image = True
            except Exception as e:
                print(e)
        app.run_code_value = s.getvalue()

        save_variables(dir(), locals(), library_names(library_lines))

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')


@socketio.on('run_code_result')
def run_code_result():
    if app.run_code_process.is_alive():
        socketio.emit('run_code_result', 'ongoing')
    else:
        if app.read_image:
            socketio.emit('read_image')
        socketio.emit('run_code_result', app.run_code_value)


def run_code_thread(source_code_base64):
    read_variables(locals())

    source_code = base64.b64decode(source_code_base64).decode('utf-8')
    message = source_code.split("\n")

    library_lines = []
    image_variables = []

    with stdoutIO() as s:
        try:
            for line in message:
                if 'import' in line:
                    library_lines.append(line)
                if '.capture(' in line:
                    variable = line.split("=")[0].replace(" ", "")
                    image_variables.append(variable)
                if '.show_image(' in line:
                    key = line.split("(")[1].split(")")[0].replace(" ", "")
                    _frame = locals()[key]
                    _frame = cv2.cvtColor(_frame, cv2.COLOR_BGR2RGB)
                    cv2.imwrite('/usr/local/lib/python3.5/dist-packages/zumidashboard/dashboard/code_editor_image.jpg',
                                _frame)
                    app.read_image = True
                # if 'def' in line:
                #     function_name = line.split('def ')[1].split('(')[0]
                #     app.code_editor_globals.append(function_name)
            co = code.compile_command(source_code, "<stdin>", "exec")
            if co:
                exec(co)
                with app.run_code_lock:
                    if app.kill_run_code_thread is True:
                        raise Exception()
        except Exception as e:
            print(e)
    app.run_code_value = s.getvalue()

    save_variables(dir(), locals(), library_names(library_lines))


def library_names(ll):
    library_list = []
    try:
        for l in ll:
            name = l.split('import ')[1].split(' ')[0]
            library_list.append(name)
    except Exception as e:
        print('error', e)

    return library_list


def save_variables(__dir, __local, ln):
    default_variables = ['co', 'line', 'message', 'script', 'source_code_base64', 's', 'library_lines',
                         'image_variables', 'source_code', 'function_name']
    # fl = app.code_editor_globals._getvalue()

    for key in __dir:
        if not key in default_variables and not key in ln:
            app.code_editor_locals[key] = __local[key]
            # print(key)
            # if key in fl:
            #     Global.key = __local[key]
            # else:
            #     app.code_editor_locals[key] = __local[key]


def read_variables(__local):
    for key in app.code_editor_locals:
        # print(key, type(key))
        __local[key] = app.code_editor_locals[key]
    # for key in app.code_editor_globals._getvalue():
    #     print(key, type(key))
    #     print(Global.key)
    #     print(__local[key])
    #     __local[key] = Global.key


@app.route('/code-editor-image/<path:filename>')
def send_image_file(filename):
    return send_from_directory('/usr/local/lib/python3.5/dist-packages/zumidashboard/dashboard', filename)


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


@socketio.on('zumi_run')
def print_message(source_code_base64):
    print('zumi run')
    message_deco = base64.b64decode(source_code_base64)
    print(message_deco)
    new_path = './blockly.py'
    new_days = open(new_path,'w+')

    new_days.write(str(message_deco, 'utf-8'))
    new_days.close()

    p1 = Thread(target = exec_thread, args = ('message_deco2',))
    p1.start()

    # await a successful emit of our reversed message
    # back to the client
    socketio.emit('robolink_run', '')


@socketio.on('check_output')
def check_output():
    print('output function')
    outputPath = './output.txt'
    try:
        outputFile = open(outputPath, 'r')
        content = outputFile.read()
        print(content)
        socketio.emit('hello', content)
    except:
        print('output file not found')


def exec_thread(message_deco):
    print(message_deco)
    try:
        exec("""\n@socketio.on('zumi_run_thread')\nasync def print_message(sid, source_code_base64):\n    global zumiprocess\nlog = open("output.txt", "w")\np = subprocess.Popen(["sudo", "python3", "blockly.py", "."],stdin=subprocess.PIPE, stdout=log, stderr=log, close_fds=True)\n\n""")
    except Exception as err:
        print("error: ", err)


@socketio.on('stop')
def stop():
    # stdoutdata = subprocess.getoutput("sudo kill $(pgrep -f blockly.py)")
    app.run_code_process.raise_exception()
    app.run_code_process.join()
    from zumi.zumi import Zumi
    zumi = Zumi()
    print("in emergency function")
    try:
        subprocess.Popen(['fuser', '-k', '3456/tcp'])
    except:
        print('streaming server is not opened')
    # socketio.emit('disconnected', {'msg': 'Connection failed!', 'status': 'false'})


# network connect -------------------------------------------------------------------------------------------
@app.route('/')
@app.route('/index')
def index():
    socketio.emit("clear_session")
    print('clear session')
    return app.send_static_file('index.html')


@app.route('/select-network')
def select_network():
    return app.send_static_file('index.html')


@app.route('/connect-network')
def connect_network():
    return app.send_static_file('index.html')


@socketio.on('no_network')
def no_network():
    app.screen.draw_text_center("Help me get online")


@socketio.on('close_network_modal')
def close_network_modal():
    app.screen.draw_text_center("")


@socketio.on('ssid_list')
def ssid_list(sid):
    print('getting ssid list')
    app.action = 'ssid_list'
    log('getting ssid list')
    if app.wifi_msg:
        app.wifi_msg = False
    wifi_dict = scripts.get_ssid_list()
    socketio.emit('ssid_list', wifi_dict)


@socketio.on('disconnect')
def test_disconnect():
    print('Socket disconnected')
    log('client disconnected')


@socketio.on('connect')
def test_connect():
    print('a client is connected')
    log('a client is connected')
    log(app.action)

    socketio.emit('language_info')

    if app.action == 'check_internet' or app.action == 'check_last_network':
        time.sleep(1)
        socketio.emit(app.action, app.action_payload)
        app.action = ''
        app.action_payload = ''


# confirm check internet msge was receive
@socketio.on('acknowledge_check_internet')
def acknowledge_check_internet():
     log('msge check internet was receive')
     app.action = ''


# refactoring
@socketio.on('connect_wifi')
def connect_wifi(ssid, passwd, isHiddenNetwork):
    print('connect wifi')
    app.internet_info = ''
    app.checked_internet = False
    app.connect_wifi_thread = ConnectWifiThread(ssid, passwd, isHiddenNetwork)
    app.connect_wifi_thread.start()


#refactoring finished
@socketio.on('connect_wifi_result')
def connect_wifi_result():
    if app.connect_wifi_thread.is_alive():
        socketio.emit('connect_wifi_result', 'in_progress')
    else:
        socketio.emit('connect_wifi_result', app.connected_wifi)


#refactoring finished
@socketio.on('stop_connect_wifi')
def stop_connect_wifi():
    try:
        print('stop connect wifi')
        app.connect_wifi_thread.raise_exception()
        app.connect_wifi_thread.join()
    except Exception as e:
        print(e)


class ConnectWifiThread(StoppableThread):
    def __init__(self, ssid, passwd, isHiddenNetwork):
        StoppableThread.__init__(self)
        self.ssid = ssid
        self.passwd = passwd
        self.isHiddenNetwork = isHiddenNetwork

    def run(self):
        print('app.py : connecting wifi start')
        log('app.py : connecting wifi start')
        app.wifi_list.clear()
        app.wifi_msg = True
        print(str(type(self.ssid)) + self.ssid)
        scripts.add_wifi(self.ssid, self.passwd, self.isHiddenNetwork)
        print("personality start")
        app.screen.draw_image_by_name("tryingtoconnect")
        sound.try_calibrate_sound(app.zumi)
        sound.try_calibrate_sound(app.zumi)
        print("personality done")
        log('app.py : connecting wifi:' + self.ssid + ' end')
        print('app.py : connecting wifi end')
        app.connected_wifi = True


#refactoring finished
@socketio.on('check_internet')
def check_internet(language):
    print('check internet')
    app.check_internet_thread = CheckInternetThread(language)
    app.check_internet_thread.start()


#refactoring finished
@socketio.on('check_internet_result')
def check_internet_result():
    if app.check_internet_thread.is_alive():
        socketio.emit('check_internet_result', 'in_progress')
    else:
        socketio.emit('check_internet_result', app.internet_info)


#refactoring finished
@socketio.on('stop_check_internet')
def stop_check_internet():
    try:
        print('stop check internet')
        app.check_internet_thread.raise_exception()
        app.check_internet_thread.join()
    except Exception as e:
        print(e)


#refactoring
class CheckInternetThread(StoppableThread):
    def __init__(self, language):
        StoppableThread.__init__(self)
        self.language = language

    def run(self):
        if app.checked_internet:
            return
        app.need_to_update = False
        print('language : ', self.language)
        set_backend_language(self.language)
        app.checked_internet = True
        connected, ssid = scripts.check_wifi()
        if not connected:
            print('wifi is not connected')
            app.internet_info = False
            return

        time.sleep(3)

        app.internet_info = scripts.check_internet(self.language, ssid)

        if app.internet_info["online_status"] == "captive":
            print('app.py: emit check internet captive portal')
            log('app.py : emit check internet captive portal')
        elif app.internet_info["can_update_dashboard"] or app.internet_info["can_update_content"]:
            app.need_to_update = True
            print('app.py: need update')
            log('app.py : need update')
        # socketio.emit(app.action, app.connected_to_internet)

        print(app.internet_info)
        # app.action_payload = app.connected_to_internet


@socketio.on('set_backend_language')
def set_backend_language(language):
    print('set backend language ', language)
    korean_key = ["kr", "ko"]
    for item in korean_key:
        if item in language:
            app.language = "ko"
            return
    else:
        app.language = "en"
    print(app.language)


@socketio.on('zumi_success')
def zumi_success():
    app.screen.draw_text_center("I'm connected to \"" + app.internet_info["network_name"] + "\"")
    sound.calibrated_sound(app.zumi)
    time.sleep(2)
    if app.need_to_update:
        app.screen.draw_text_center("I can update")
    time.sleep(1)
    # _awake()


@socketio.on('kill_supplicant')
def kill_supplicant():
    scripts.kill_supplicant()


@socketio.on('zumi_fail')
def zumi_fail():
    app.screen.draw_text_center("Failed to connect.\n Try again.")
    app.zumi.play_note(Note.A5, 100)
    app.zumi.play_note(Note.F5, 2 * 100)
    time.sleep(2)
    app.screen.draw_text_center("Go to \"zumidashboard.ai\" in your browser")


@socketio.on('open_eyes')
def open_eyes():
    app.screen.hello()


# zumi run demo and lesson event link is in frontend already
@socketio.on('activate_offline_mode')
def activate_offline_mode():
    app.internet_info = ''
    app.checked_internet = False
    # usr_dir_path = "/home/pi/Dashboard/off"
    app.screen.draw_text_center("Starting offline mode")
    subprocess.Popen(['sudo', 'killall', 'wpa_supplicant'])
    time.sleep(2)
    # if app.user != "":
    #     app.user = ""
    #     subprocess.call(['sudo', 'pkill', '-9', 'jupyter'])
    #     time.sleep(1)
    #     subprocess.call(['sudo', 'bash', lib_dir + '/shell_scripts/jupyter.sh', usr_dir_path])


@socketio.on('view_logs')
def view_logs():
    p = subprocess.Popen('sudo journalctl -u zumidashboard.service > /usr/local/lib/python3.5/dist-packages/zumidashboard/dashboard/log.txt',
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    p.communicate()
    with open('/usr/local/lib/python3.5/dist-packages/zumidashboard/dashboard/log.txt', 'r') as file_data:
        output = ""
        for line in file_data:
            output += line
    socketio.emit('view_logs', output)


# are we use this?? ----------------------------------------------------------------------------
@socketio.on('run_demos')
def run_demos():
    print('Run demos event from dashboard')


@socketio.on('goto_lessons')
def goto_lessons():
    print('Go to lessons event from dashboard')


# updater ----------------------------------------------------------------------------------------------------
def __set_updateconf(_version="develop", _language="None"):
    with open("/etc/.updateconf", "w") as update_info:
        update_info.write("args1={}\n".format(_version))
        update_info.write("args2={}".format(_language))

@app.route('/update')
def update():
    return app.send_static_file('index.html')


@socketio.on('update_firmware')
def update_firmware():
    print('update firmware from dashboard')
    version = re.findall('[0-9]+.[0-9]+', app.internet_info["latest_dashboard_version"])[0]
    __set_updateconf(_version=version)
    subprocess.Popen(['sudo', 'systemctl', 'start', 'zumi_updater.service'])


@socketio.on('update_everything')
def update_everything():
    print('update firmware & content from dashboard')
    version = re.findall('[0-9]+.[0-9]+', app.internet_info["latest_dashboard_version"])[0]
    __set_updateconf(_version=version, _language=app.language)
    subprocess.Popen(['sudo', 'systemctl', 'start', 'zumi_updater.service'])


@socketio.on('update_content')
def update_content():
    print('update content from dashboard')
    app.check_update_content = False
    updater.update_content(app.zumi, app.screen, app.language)
    app.check_update_content = True


@socketio.on('check_update_content')
def check_update_content():
    print(app.check_update_content)
    socketio.emit('check_update_content', app.check_update_content)


@socketio.on('check_content_missing')
def check_content_missing():
    check_content = scripts.check_content_missing(app.language)
    socketio.emit('check_content_missing', check_content)


@socketio.on('check_user_content_missing')
def check_user_content_missing():
    print('check user content missing')
    check_user_content = scripts.check_user_content_missing(app.user, app.language)
    socketio.emit('check_user_content_missing', check_user_content)
    print(check_user_content)


@socketio.on('update_true')
def update_true():
    app.screen.draw_text_center("I can update")


@socketio.on('update_false')
def update_false():
    app.screen.hello()


# for check OS/setup update
def firmware_updater_check(base):
    print("checker")
    if not os.path.isdir(base+'update'):
        os.mkdir(base+'update')
    if not os.path.isfile(base+'update/update_log.txt'):
        f = open(base+'update/update_log.txt','w')
        f.close()

    try:
        update_list = os.listdir(lib_dir + '/update_scripts/')
        for line in open(base + 'update/update_log.txt'):
            try:
                update_list.remove(line.rstrip('\n'))
            except:
                pass

    except FileNotFoundError:
        update_list = []

    if len(update_list):
        firmware_updater(update_list)
        return "updated"
    else:
        return "no update"


# for check OS/setup update
def firmware_updater(update_list):
    print(update_list)
    update_list.sort()
    print(update_list)
    f = open('/home/pi/Dashboard/update/update_log.txt', 'a')
    for version in update_list:
        print("update {}".format(version))
        p = subprocess.Popen(
            ['sudo', 'sh', lib_dir + '/update_scripts/'+version, '.'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        stdout, stderr = p.communicate()
        p.wait()
        f.write(version+"\n")


@app.route('/develop')
def develop():
    print('update develop firmware from dashboard')
    __set_updateconf()
    subprocess.Popen(['sudo', 'systemctl', 'start', 'zumi_updater.service'])
    return app.send_static_file('index.html')


# main dashboard page related ---------------------------------------------------------------------------------
@app.route('/main')
def step2():
    return app.send_static_file('index.html')


@app.route('/shutting-down')
def shutting_down():
    return app.send_static_file('index.html')


@app.route('/learn')
def learn():
    # update_lessonlist_file()
    return app.send_static_file('index.html')


@app.route('/learn-code-editor')
def learn_code_editor():
    return app.send_static_file('index.html')


@app.route('/explore')
def explore():
    return app.send_static_file('index.html')


@app.route('/zumiterminal-8585677100')
def zumiterminal():
    subprocess.call(['sudo', 'bash', lib_dir + '/shell_scripts/jupyter.sh', "/home/pi/Desktop"])
    time.sleep(1)
    while True:
        time.sleep(3)
        p = subprocess.Popen(
            ['sudo', 'bash', lib_dir + '/shell_scripts/check_port.sh', '5555'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        stdout, stderr = p.communicate()
        p.wait()
        if len(stdout) > 1:
            print('jupyter server is not ready')
        else:
            print('jupyter server is ready')
            break

    return "Jupyter has started. <br><br>" \
           "Please go to <a href=\"http://zumidashboard.ai:5555/terminals/1\">" \
           "http://zumidashboard.ai:5555/terminals/1</a> to access the terminal<br>" \
           "Or go to <a href=\"http://zumidashboard.ai:5555\">http://zumidashboard.ai:5555</a> to access Jupyter"


@socketio.on('change_language')
def change_language(language):
    set_backend_language(language)
    try:
        dump_lesson_json(app.user)
    except:
        if app.user != '':
            subprocess.call(['cp', lib_dir + '/shell_scripts/LessonList.json',
                             lib_dir+'/dashboard'])
        print("folder not found")


@socketio.on('shutdown')
def shutdown():
    app.screen.draw_text_center("Please switch off after 15 seconds.")
    scripts.shutdown()


@socketio.on('reboot')
def reboot():
    app.screen.draw_text_center("Reboot")
    subprocess.call(['sudo', 'reboot'])


@socketio.on('battery_percent')
def battery_percent():
   socketio.emit('battery_percent',str(app.zumi.get_battery_percent()))


@socketio.on('hardware_info')
def hardware_info():
    import psutil, uuid
    from gpiozero import CPUTemperature

    cpu_info = str(int(psutil.cpu_percent()))
    ram_info = str(int(psutil.virtual_memory().percent))
    mac_address = str(':'.join(re.findall('..', '%012x' % uuid.getnode())))
    cpu_temp = CPUTemperature(min_temp=50, max_temp=90)
    cpu_temp_info = str(int(cpu_temp.temperature))
    try:
        with open('/home/pi/Dashboard/Zumi_Content_{}/README.md'.format(app.language), 'r') as zumiContentVersionFile:
            content_version = zumiContentVersionFile.readline().replace("\n", "")
    except:
        content_version = ''
    board_version = str(app.zumi.get_board_firmware_version())

    hardward_info = {"cpu_info": cpu_info, "ram_info": ram_info, "mac_address": mac_address,
                     "cpu_temp": cpu_temp_info, "content_version": content_version, "board_version": board_version}

    socketio.emit('hardware_info', hardward_info)
    socketio.emit('battery_percent', str(app.zumi.get_battery_percent()))


# lesson page
@socketio.on('update_lessonlist_file')
def update_lessonlist_file(usr_name):
    dump_lesson_json(usr_name)


@socketio.on('update_new_lessonlist_file')
def update_new_lessonlist_file():
    if app.language == "ko":
        print('Korean content does not have code editor version yet')
        return

    p = subprocess.Popen(['sudo', 'chown', '-R', 'pi:pi', "/home/pi/Dashboard/user/{}".format(app.user)])
    p.communicate()
    print("update new lesson json")
    lesson_files_path = "/home/pi/Dashboard/user/{}/Zumi_Content_{}/NewLesson/".format(app.user, app.language)
    lesson_folder_files = os.listdir(lesson_files_path)
    lesson_folder_files.sort()
    lesson_list = []
    lesson_id = 0
    for lesson_name in lesson_folder_files:
        if lesson_name[-2:] == 'md':
            lesson_info = {"id": lesson_id, "title": lesson_name[:-3], "description": lesson_name[:-3] + " (code editor)"}
            lesson_list.append(lesson_info)
            lesson_id += 1
    json_data = {"LessonList": lesson_list}
    with open('{}/dashboard/NewLessonList.json'.format(lib_dir), 'w') as lesson_list_json_file:
        json.dump(json_data, lesson_list_json_file)


def dump_lesson_json(usr_name):
    p = subprocess.Popen(['sudo', 'chown', '-R', 'pi:pi', "/home/pi/Dashboard/user/{}".format(usr_name)])
    p.communicate()
    print("update lesson json")
    lesson_files_path = "/home/pi/Dashboard/user/{}/Zumi_Content_{}/Lesson/".format(usr_name, app.language)
    lesson_folder_files = os.listdir(lesson_files_path)
    lesson_folder_files.sort()
    lesson_list = []
    lesson_id = 0
    for lesson_name in lesson_folder_files:
        if lesson_name[-5:] == 'ipynb':
            with open(lesson_files_path + lesson_name, 'r') as lesson_file:
                file_content = json.loads(lesson_file.read())
            try:
                description = ""
                for p in file_content["cells"][1]["source"]:
                    p = re.sub(r'#+', '', p)
                    description += re.sub(r'<.*?>', '', p)
                    if len(description) > 175:
                        description = description[:175] + "..."
                        break
            except:
                print("something is happen to generate json file")
                description = " "
            lesson_info = {"id": lesson_id, "title": lesson_name[:-6], "description": description}
            lesson_list.append(lesson_info)
            lesson_id += 1
    json_data = {"LessonList": lesson_list}
    with open('{}/dashboard/LessonList.json'.format(lib_dir), 'w') as lesson_list_json_file:
        json.dump(json_data, lesson_list_json_file)

# TODO decide way to send multiple way
# we can make sending with tag as well
@socketio.on('read_lesson_file')
def read_lesson_file(lesson_name):
    file_content = ""
    file_path = '/home/pi/Dashboard/user/' + app.user + '/Zumi_Content_en/NewLesson/' + lesson_name + ".md"
    with open(file_path) as lesson:
        for line in lesson.readlines():
            file_content += line
    # # option 1 send through socket directly
    socketio.emit("read_lesson_file", file_content.split("***\n"))
    # socketio.emit("read_lesson_file", {"lesson": file_content})
    # # option 2
    # with open('someware current lesson file read', 'w') as lesson_json:
    #     json.dump({"lesson": file_content}, lesson_json)

# multiple user ----------------------------------------------------------------------------------------------------
@app.route('/login')
def login():
    return app.send_static_file('index.html')


@socketio.on('get_users')
def get_users():
    # this is not happen but put in here
    if not os.path.isdir(usr_dir):
        os.makedirs(usr_dir)
    usr_list = os.listdir(usr_dir)
    app.screen.draw_text_center("Please sign in")
    socketio.emit('get_users', usr_list)


@socketio.on('add_user')
def add_user(usr_name):
    add_usr_dir = usr_dir + usr_name
    if os.path.isdir(add_usr_dir):
        # socketio.emit(add_user, False)
        print("user is already exist")
    else:
        os.makedirs(add_usr_dir)
        os.mkdir(add_usr_dir + '/My_Projects')
        os.mkdir(add_usr_dir + '/My_Projects/Jupyter')
        os.mkdir(add_usr_dir + '/My_Projects/Blockly')

        with open("{}/.overlay.json".format(add_usr_dir), "w") as json_file:
            overlaydata = dict()
            overlaydata["main"] = True
            overlaydata["learn"] = True
            json.dump(overlaydata, json_file)
        # for multiple user updater
        # app.copy_content = subprocess.Popen(['cp', '-r', '/home/pi/Dashboard/Zumi_Content_'+app.language, add_usr_dir])
        # p.communicate()
        print("generate user : {}".format(usr_name))
        # socketio.emit(add_user, True)


@socketio.on('check_add_user')
def check_add_user():
    if app.copy_content != '':
        poll = app.copy_content.poll()
    else:
        socketio.emit("check_add_user", False)
        return

    if poll is None:
        socketio.emit("check_add_user", False)
    else:
        socketio.emit("check_add_user", True)


@socketio.on('check_overlay')
def check_overlay(user_name):
    current_usr_dir = usr_dir + user_name
    with open("{}/.overlay.json".format(current_usr_dir), "r") as json_file:
        overlay_data = json.load(json_file)
        print(overlay_data)
    socketio.emit('check_overlay', overlay_data)


@socketio.on('start_user')
def start_user(usr_name):
    base_dir_path = "/home/pi/Dashboard/"
    usr_dir_path = base_dir_path + 'user/' + usr_name + '/'

    if app.user != usr_name:
        app.user = usr_name
        subprocess.call(['sudo', 'pkill', '-9', 'jupyter'])
        time.sleep(1)
        subprocess.call(['sudo', 'bash', lib_dir + '/shell_scripts/jupyter.sh', usr_dir_path])
    app.screen.draw_text_center("Hello, {}!".format(usr_name))
    time.sleep(1)
    _awake()

    if updater.check_user_content(base_dir_path, usr_dir_path, app.language):
        socketio.emit("need_update_user_content", True)
        print("start updating user's content")
        time.sleep(3)
        app.update_user_content_thread = Thread(target=updater.copy_content, args=(base_dir_path, usr_dir_path, app.language))
        app.update_user_content_thread.start()
    else:
        socketio.emit("need_update_user_content", False)
    try:
        dump_lesson_json(usr_name)
    except:
        subprocess.call(['cp', lib_dir + '/shell_scripts/LessonList.json',
                         lib_dir + '/dashboard'])
    # maybe printout something on zumi or reaction


@socketio.on('check_update_user_content_done')
def check_update_user_content_done():
    if app.update_user_content_thread.is_alive():
        socketio.emit('check_update_user_content_done', False)
    else:
        socketio.emit('check_update_user_content_done', True)


@socketio.on('change_user_name')
def change_user_name(user_names):
    previous_user_dir = usr_dir + user_names[0]
    new_user_dir = usr_dir + user_names[1]
    # if changing name is already exist
    if os.path.isdir(new_user_dir):
        # socketio.emit('change_user_name', False)
        print("changing name {} is already".format(user_names[1]))
    # if current name is not exist
    elif not os.path.isdir(previous_user_dir):
        # socketio.emit('change_user_name', False)
        print("current user {} is not exist".format(user_names[0]))
    else:
        subprocess.Popen(['mv', previous_user_dir, new_user_dir])
        # socketio.emit('change_user_name', False)
        print("change user {} to {}".format(user_names[0], user_names[1]))


@socketio.on('delete_user')
def delete_user(user_name):
    delete_usr_dir = usr_dir + user_name;
    if os.path.isdir(delete_usr_dir):
        subprocess.Popen(['rm', '-r', delete_usr_dir])
        print("user {} is deleted".format(user_name))
        # socketio.emit('delete_user', True)
    else:
        print("user {} is not exist or already deleted".format(user_name))
        # socketio.emit('delete_user', False)

# ---might use later----
# def generate_guest_user():
#     guest_usr_dir = usr_dir + 'guest'
#     os.mkdir(guest_usr_dir)
#     os.mkdir(guest_usr_dir + '/My_Projects')
#     os.mkdir(guest_usr_dir + '/My_Projects/Jupyter')
#     os.mkdir(guest_usr_dir + '/My_Projects/Blockly')
#     subprocess.Popen(['cp', '-r', '/home/pi/Dashboard/Zumi_Content', guest_usr_dir])
#     subprocess.Popen(['sudo', 'chown', '-R', 'pi', guest_usr_dir])


@socketio.on('check_jupyter_server')
def check_jupyter_server():
    p = subprocess.Popen(
        ['sudo', 'bash', lib_dir + '/shell_scripts/check_port.sh', '5555'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    stdout, stderr = p.communicate()
    p.wait()
    if len(stdout) > 1:
        print('jupyter server is not ready')
        socketio.emit('check_jupyter_server', False)
    else:
        print('jupyter server is ready')
        socketio.emit('check_jupyter_server', True)


@socketio.on('overlay_change')
def overlay_change(user_name, item):
    current_usr_dir = usr_dir + user_name
    json_file = open('{}/.overlay.json'.format(current_usr_dir), 'r')
    overlay_data = json.load(json_file)
    overlay_data[item] = False
    json_file.close()
    print(overlay_data)
    with open('{}/.overlay.json'.format(current_usr_dir), 'w') as json_file:
        json.dump(overlay_data, json_file)


# drive mode --------------------------------------------------------------------------------------------------------
@app.route('/drive-mode')
def drive():
    return app.send_static_file('index.html')


@socketio.on('open_pi_streaming')
def open_pi_streaming():
    app.opening_streaming_server_proc = subprocess.Popen(
        ['python3', os.path.dirname(os.path.abspath(__file__)) + '/webstreaming.py', '--protocol', 'http'])


@socketio.on('check_camera_connection')
def check_camera_connection():
    try:
        subprocess.Popen(['fuser', '-k', '3456/tcp'])
        time.sleep(1)
    except:
        print('streaming server was not opened')

    from zumi.util.camera import Camera

    try:
        camera = Camera(auto_start=True)
        frame = camera.capture()
        camera.close()
        socketio.emit('check_camera_connection', True)
    except:
        socketio.emit('check_camera_connection', False)


@socketio.on('check_streaming_server')
def check_streaming_server():
    p = subprocess.Popen(
        ['sudo', 'bash', lib_dir + '/shell_scripts/check_port.sh', '3456'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    stdout, stderr = p.communicate()
    p.wait()
    if len(stdout) > 1:
        print('streaming server is not ready')
        socketio.emit('check_streaming_server', False)
    else:
        print('streaming server is ready')
        socketio.emit('check_streaming_server', True)


@socketio.on('stop_motors')
def stop_motors():
    app.zumi = Zumi()


@socketio.on('zumi_direction')
def zumi_direction(input_key):
    app.drive_mode.zumi_direction(input_key)

@socketio.on('zumi_celebrate')
def zumi_celebrate():
    app.screen.clear()
    app.personality.celebrate()
    Thread(target=drive_open_eyes, args=(5,)).start()

@socketio.on('zumi_happy')
def zumi_happy():
    app.screen.clear()
    app.personality.happy()
    Thread(target=drive_open_eyes, args=(5,)).start()

@socketio.on('zumi_awake')
def zumi_awake():
    app.screen.clear()
    app.personality.awake()
    Thread(target=drive_open_eyes, args=(5,)).start()

@socketio.on('zumi_angry')
def zumi_angry():
    app.screen.clear()
    app.personality.angry()
    Thread(target=drive_open_eyes, args=(5,)).start()

@socketio.on('zumi_stop')
def zumi_stop():
    app.drive_mode.zumi_stop()


@socketio.on('display_text')
def display_text(txt):
    app.screen.clear()
    sound.calibrated_sound(app.zumi)
    if txt == '':
        app.screen.hello()
        return
    app.screen.draw_text_center(txt)
    Thread(target=drive_open_eyes, args=(15,)).start()


def drive_open_eyes(t):
    time.sleep(t)
    app.screen.clear()
    app.screen.hello()


@socketio.on('camera_stop')
def camera_stop():
    print('camera should be stopped')
    subprocess.Popen(['fuser', '-k', '3456/tcp'])
    subprocess.Popen(['fuser', '-k', '9696/tcp'])

    try:
        app.opening_streaming_server_proc.kill()
        print('Kill opening streaming server')
    except:
        print('There was no opening streaming server')


# code mode --------------------------------------------------------------------------------------------------------
@app.route('/code-mode')
def code_mode():
    return app.send_static_file('index.html')


@socketio.on('code_mode')
def code_mode(user_name):

    blockly = os.listdir(usr_dir + '/' + user_name + '/My_Projects/Blockly')
    jupyter = [file.split(".ipynb")[0] for file in os.listdir(usr_dir + '/' + user_name + '/My_Projects/Jupyter') if
               file.endswith(".ipynb")]
    # #code for return [tag, project_name]
    # for x in len(project_list):
    #     tag = re.findall('<[a-z]+>', project_list[x])[0]
    #     project_list[x] = [tag, project_list[x].replace(tag,'')]
    socketio.emit('code_mode', {"jupyter": jupyter, "blockly": blockly})


@socketio.on('create_jupyter')
def create_jupyter(user_name, project_name):
    jupyter_folder = "{}/My_Projects/Jupyter/".format(usr_dir + user_name)
    subprocess.call(['cp', lib_dir + '/shell_scripts/Untitled.ipynb', jupyter_folder])
    time.sleep(1)
    subprocess.call(['mv', "{}Untitled.ipynb".format(jupyter_folder), "{}{}.ipynb".format(jupyter_folder, project_name)])
    time.sleep(1.5)
    subprocess.Popen(['sudo', 'chown', '-R', 'pi', jupyter_folder])


@socketio.on('get_blockly_project')
def get_blockly_project(user_name, selected_project):
    print('app: get xml project')
    if app.new_blockly_project:
        app.new_blockly_project = False
        socketio.emit('get_blockly_project', '')
    else:
        project_file = open("{}/My_Projects/Blockly/{}.xml".format(usr_dir + user_name, selected_project), 'r')
        socketio.emit('get_blockly_project', str(project_file.read()))


@socketio.on('save_blockly_file')
def save_blockly_file(user_name, project_name, xml_content):
    print('app: saving blockly file')
    myfile = open("{}/My_Projects/Blockly/{}.xml".format(usr_dir + user_name, project_name), 'w')
    myfile.write(xml_content)
    myfile.close()


@socketio.on('create_blockly')
def create_blockly(user_name, project_name):
    app.new_blockly_project = True
    # need to copy from blank project xml file
    myfile = open("{}/My_Projects/Blockly/{}.xml".format(usr_dir + user_name, project_name), 'w')
    myfile.close()


@socketio.on('rename_blockly')
def rename_blockly(user_name, project_name, new_name):
    blockly_dir = "{}/My_Projects/Blockly/".format(usr_dir + user_name)
    subprocess.call(['mv', "{}.xml".format(blockly_dir+project_name), "{}.xml".format(blockly_dir+new_name)])
    time.sleep(1)

@socketio.on('rename_jupyter')
def rename_jupyter(user_name, project_name, new_name):
    jupyter_dir = "{}/My_Projects/Jupyter/".format(usr_dir + user_name)
    subprocess.call(['mv', "{}.ipynb".format(jupyter_dir+project_name), "{}.ipynb".format(jupyter_dir+new_name)])
    time.sleep(1)

@socketio.on('delete_blockly')
def delete_blockly(user_name, project_name):
    blockly_dir = "{}/My_Projects/Blockly/".format(usr_dir + user_name)
    subprocess.call(['rm',"-rf", "{}.xml".format(blockly_dir + project_name)])
    time.sleep(1)

@socketio.on('delete_jupyter')
def delete_jupyter(user_name, project_name):
    blockly_dir = "{}/My_Projects/Jupyter/".format(usr_dir + user_name)
    subprocess.call(['rm',"-rf", "{}.ipynb".format(blockly_dir + project_name)])
    time.sleep(1)


# wizards -------------------------------------------------------------------------------------------------
@app.route('/learning-drive-distance')
def learning_drive_distance():
    return app.send_static_file('index.html')


@socketio.on('drive_regression')
def drive_regression(seconds):
    app.zumi.forward(duration=seconds)


@socketio.on('recalibrate')
def recalibrate():
    app.screen.draw_text_center("Place me on\na flat surface.", font_size=18)
    sound.happy_sound(app.zumi)
    time.sleep(5)
    app.screen.calibrating()
    sound.try_calibrate_sound(app.zumi)
    app.zumi.calibrate_gyro()
    time.sleep(3)
    app.screen.draw_image_by_name("calibrated")
    sound.calibrated_sound(app.zumi)
    time.sleep(5)
    app.screen.hello()



@app.route('/learning-colors')
def learning_colors():
    return app.send_static_file('index.html')


@socketio.on('start_learning_color')
def start_learning_color():
    from zumi.util.color_classifier import ColorClassifier
    app.knn = ColorClassifier(path='/home/pi/Dashboard/user/'+app.user+'/Data')
    app.knn.demo_name = "tmp"
    app.knn.data_file_name = app.knn.demo_name + "_KNN_data"


@socketio.on('learning_color_label_list')
def learning_color_label_list(label_list):
    print(label_list)
    app.knn.label_num = len(label_list)
    for label in label_list:
        app.knn.label_names.append(label)
        app.knn.label_keys.append(label)


@socketio.on('add_color_data')
def add_color_data(label_name):
    app.knn.current_label = label_name
    app.knn.label_cnt += 1
    try:
        feature = cv2.imread('/home/pi/Dashboard/DriveImg/drivescreen.jpg')

        if not isinstance(feature, list):
            feature = app.knn.get_hsv_data(feature)

        if feature == [20,0,128]:
            socketio.emit('add_color_data_result', False)
            return

        app.knn.labels.append(label_name)
        app.knn.features.append(feature)
        if label_name in app.knn.data_cnt.keys():
            app.knn.data_cnt[label_name] += 1
        else:
            app.knn.data_cnt[label_name] = 1
        socketio.emit('add_color_data_result', feature)
    except:
        socketio.emit('add_color_data_result', False)


@socketio.on('color_train')
def color_train():
    print(app.knn.label_num)
    app.knn.save_data_set()
    app.knn.get_accuracy()


@socketio.on('knn_fit_hsv')
def knn_fit_hsv():
    app.knn.fit("hsv")


@socketio.on('color_predict')
def color_predict():
    try:
        image = cv2.imread('/home/pi/Dashboard/DriveImg/drivescreen.jpg')
        predict = app.knn.predict(image)
        if not isinstance(image, list):
            feature = app.knn.get_hsv_data(image)
        print(predict, feature)
        socketio.emit('color_predict', {"label": predict, "feature": feature})
    except:
        print('error')


@socketio.on('knn_save_model')
def knn_save_model(model_name):
    print(model_name)
    app.knn.demo_name = model_name
    app.knn.data_file_name = model_name + "_KNN_data"
    app.knn.save_data_set()


@app.route('/learning-face-detection')
def learning_face_detection():
    return app.send_static_file('index.html')


# main ----------------------------------------------------------------------------------------------------
def run(_debug=False):
    if not os.path.isfile('/usr/local/lib/python3.5/dist-packages/zumidashboard/dashboard/hostname.json'):
        subprocess.run(["sudo ln -s /etc/hostname /usr/local/lib/python3.5/dist-packages/zumidashboard/dashboard/hostname.json"], shell=True)
    firmware_updater_check('/home/pi/Dashboard/')

    p = subprocess.Popen(
        ['sudo', 'bash', lib_dir + '/shell_scripts/check_port.sh', '8443'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    stdout, stderr = p.communicate()
    p.wait()
    if len(stdout) > 1:
        p = subprocess.run('sudo python3 /usr/local/lib/python3.5/dist-packages/zumidashboard/gesture.py & 2>&1', shell=True)

    socketio.run(app, debug=_debug, host='0.0.0.0', port=80)


if __name__ == '__main__':
    run()

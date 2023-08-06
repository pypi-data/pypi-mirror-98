""" Лаунчер Gravity interface """


from gravity_interface.configs.settings import Settings

from gravity_interface.main_operator import *
from gravity_interface.wlistener import WListener
from gravity_interface.tools.screenRes import ScreenRes
from traceback import format_exc
from gravity_interface.styles import color_solutions as cs


deffaultScreenSize = ScreenRes.get()
dirpath = os.path.dirname(os.path.realpath(__file__))
img_dir = os.path.join(dirpath, 'imgs')
loadingWin = os.path.join(img_dir, 'loadingWin.png')
print('path', loadingWin)

root = Tk()
root.grab_set()
root.focus_set()
root.overrideredirect(True)
root.geometry("600x350-{}-{}".format(500, 300))
loadingcan = Canvas(root, highlightthickness=0)
loadingcan.pack(fill=BOTH,expand=YES)
photoimg = PhotoImage(file=loadingWin)
loadingcan.create_image(600/2,350/2, image=photoimg)

from gravity_interface.styles.styles import *

def startLoading():
    '''Инициализация проекта, выполняется параллельно с окном загрузки'''
    root.grab_set()
    root.focus_set()
    settings = Settings(root, dirpath)
    wlistener = WListener('Въезд', 'COM1', 9600)
    can = Canvas(root, highlightthickness=0, bg=cs.main_background_color)
    operator = Operator(root, settings, wlistener, can,
        deffaultScreenSize)
    loadingcan.destroy()
    root.overrideredirect(False)
    root.attributes('-fullscreen', True)
    print(settings.project_name,'был загружен.')
    can.pack(fill=BOTH,expand=YES)
    ScreenRes.set(1366,768)
    root.geometry("{0}x{1}-0-0".format(root.winfo_screenwidth(),
        root.winfo_screenheight()))

def startLoadingThread():
    '''Запуск инициализации загрузки параллельным потоком'''
    threading.Thread(target=startLoading, args=()).start()

def launch_mainloop():
    """ Запустить оснвной цикл работы """
    root.after(100, startLoadingThread)
    try:
        root.mainloop()
    except:
        # При выходе из программы - трассировать текст исключения и выполнить
        # необходимые завершающие работы
        print(format_exc())
        os._exit()
    ScreenRes.set(deffaultScreenSize)

launch_mainloop()
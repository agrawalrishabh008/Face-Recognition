import tkinter as tk
import util
from PIL import Image, ImageTk
import cv2
import os.path
import subprocess
import datetime
import webbrowser



class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+80+108")

        self.login_button_main_window = util.get_button(self.main_window, 'लॉग इन', 'green', self.login)
        self.login_button_main_window.place(x=850, y=330)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'नया उपयोगकर्ता पंजीकृत करें', 'gray', self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=700, y=430, width=500)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=10, width=780, height=400)

        self.add_webcam(self.webcam_label)

        self.db_dir = "db"

        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = 'log.txt'


    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame

        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)

        self.most_recent_capture_pil = Image.fromarray(img_)

        imgtk = ImageTk.PhotoImage(image = self.most_recent_capture_pil)

        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def login(self):
        unknown_img_path = 'tmp.jpg'

        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
        # print(output)
        name = output.split(',')[1][:-5]
        print(name)

        if name in ["unknown_person", "no_persons_found"]:
            util.msg_box('चेतावनी!!!...', 'अज्ञात उपयोगकर्ता। कृपया नया उपयोगकर्ता पंजीकृत करें या पुनः प्रयास करें')
        else:
            util.msg_box('वापसी पर स्वागत है!', 'स्वागत, {}.'.format(name))
            with open(self.log_path, 'a') as f:
                f.write('{} {}\n'.format(name, datetime.datetime.now()))
                f.close()
                os.remove(unknown_img_path)
                # self.main_window.destroy()
                webbrowser.open("http://10.5.178.203:3000/query")
                webbrowser.open("http://10.5.178.203:3000/")


        os.remove(unknown_img_path)

    # def login(self):
    #     unknown_img_path = 'tmp.jpg'
    #     cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)
    #
    #     # Ensure to modify this path depending on your operating system specifics
    #     face_recognition_path = os.path.join(os.environ['VIRTUAL_ENV'], 'Scripts', 'face_recognition.exe')
    #
    #     try:
    #         output = subprocess.check_output([face_recognition_path, self.db_dir, unknown_img_path])
    #         output = output.decode()  # Decode bytes to string
    #         name = output.split(',')[1][:-5].strip()
    #         print(name)
    #
    #         if name in ["unknown_person", "no_persons_found"]:
    #             util.msg_box('चेतावनी!!!...',
    #                          'अज्ञात उपयोगकर्ता। कृपया नया उपयोगकर्ता पंजीकृत करें या पुनः प्रयास करें')
    #         else:
    #             util.msg_box('वापसी पर स्वागत है!', 'स्वागत, {}.'.format(name))
    #             with open(self.log_path, 'a') as f:
    #                 f.write('{} {}\n'.format(name, datetime.datetime.now()))
    #
    #             # Assuming these URLs are to be opened after successful login
    #             webbrowser.open("http://10.5.178.203:3000/query")
    #             webbrowser.open("http://10.5.178.203:3000/")
    #     except subprocess.CalledProcessError as e:
    #         print("Face recognition process failed with exit status:", e.returncode)
    #         print("Output:", e.output.decode())
    #     except FileNotFoundError:
    #         print(f"Command not found: {face_recognition_path}. Please check the path.")
    #     except Exception as e:
    #         print("An unexpected error occurred:", str(e))
    #     finally:
    #         if os.path.exists(unknown_img_path):
    #             os.remove(unknown_img_path)


    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+80+108")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'स्वीकार', 'green',
                                                                      self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=850, y=330)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'पुनः प्रयास करें',
                                                                         'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=850, y=430)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=10, width=780, height=400)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window,
                                                                'कृपया, अपना उपयोगकर्ता \nनाम लिखें :')
        self.text_label_register_new_user.place(x=750, y=70)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")

        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_user_capture)

        util.msg_box('सफलता!', 'उपयोगकर्ता सफलतापूर्वक पंजीकृत किया गया था!')

        self.register_new_user_window.destroy()


if __name__ == "__main__":
    app = App()
    app.start()

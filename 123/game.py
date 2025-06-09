import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import pygame


#Quản lý trạng thái của thú cưng
class Critter:
    def __init__(self, name):
        self.name = name
        self.hunger = 0
        self.boredom = 0
        pygame.mixer.init()


#thời gian trôi qua
    def __pass_time(self):
        self.hunger += 1
        self.boredom += 1

# 🍽️ ăn, 🎮 chơi, 💤 ngủ
    def eat(self):
        self.hunger = max(0, self.hunger - 4)
        self.__pass_time()

    def play(self):
        self.boredom = max(0, self.boredom - 4)
        self.__pass_time()

    def sleep(self):
        self.hunger += 1  # Ngủ <=> +1 Đói
        self.boredom = max(0, self.boredom - 2)
        self.__pass_time()

#Hiển thị trạng thái
    def get_status(self):
        return f"Tên: {self.name} | Đói: {self.hunger} | Buồn chán: {self.boredom}"

#Import giao diện 
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence


class CritterApp:
    def __init__(self, root): #Thiết kế giao diện
        self.root = root
        self.root.title("Critter Caretaker")

        self.critter = None

        # Widgets
        self.name_label = tk.Label(root, text="Nhập tên thú cưng:")
        self.name_label.pack()

        self.name_entry = tk.Entry(root)
        self.name_entry.pack()

        self.create_button = tk.Button(root, text="Tạo", command=self.create_critter)
        self.create_button.pack(pady=5)

        self.feed_button = tk.Button(root, text="Cho ăn", command=self.feed_critter)
        self.feed_button.pack(pady=2)

        self.play_button = tk.Button(root, text="Chơi", command=self.play_with_critter)
        self.play_button.pack(pady=2)

        self.sleep_button = tk.Button(root, text="Ngủ", command=self.critter_sleep)
        self.sleep_button.pack(pady=2)

        self.status_label = tk.Label(root, text="Chưa có thú nào được tạo.")
        self.status_label.pack(pady=10)
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)
# Load ảnh mặc định lúc đầu (idle)
        self.load_gif("idle.gif")

#Các hoạt động
    def create_critter(self):
        name = self.name_entry.get().strip()
        if name:
            self.critter = Critter(name)
            self.update_status()
        else:
            messagebox.showwarning("Lỗi", "Vui lòng nhập tên!")
        self.load_gif("idle.gif")


    def feed_critter(self):
        if self.critter:
            self.critter.eat()
            self.update_status()
            self.play_sound("eating.wav")
        else:
            self.show_error()
        self.load_gif("eating.gif")
           

    def play_with_critter(self):
        if self.critter:
            self.critter.play()
            self.update_status()
            self.play_sound("playing.wav")
        else:
            self.show_error()
        self.load_gif("playing.gif")


    def critter_sleep(self):
        if self.critter:
            self.critter.sleep()
            self.update_status()
            self.play_sound("sleeping.wav")
        else:
            self.show_error()
        self.load_gif("sleeping.gif")


    def update_status(self):
        self.status_label.config(text=self.critter.get_status())

    def show_error(self):
        messagebox.showerror("Lỗi", "Bạn chưa tạo thú cưng!")

    def load_gif(self, path):
        self.frames = []
        self.delays = []  # Thêm danh sách lưu thời gian delay giữa các frame

        try:
            img = Image.open(path)
            for frame in ImageSequence.Iterator(img):
                duration = frame.info.get('duration', 100)  # ms, mặc định 100ms nếu không có
                frame = frame.resize((150, 150))
                self.frames.append(ImageTk.PhotoImage(frame.copy()))
                self.delays.append(duration)
            self.current_frame = 0
            self.animate()
        except Exception as e:
            print("Lỗi khi load ảnh GIF:", e)


    def animate(self):
        if self.frames:
            frame = self.frames[self.current_frame]
            delay = self.delays[self.current_frame]  # Lấy delay đúng với frame
            self.image_label.config(image=frame)
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.root.after(delay, self.animate)  # Lặp lại theo thời gian delay của từng frame
    
    def play_sound(self, file):
        try:
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()
        except Exception as e:
            print("Không thể phát âm thanh:", e)


#Chạy chương trình 
if __name__ == "__main__":
    root = tk.Tk()
    app = CritterApp(root)
    root.mainloop()



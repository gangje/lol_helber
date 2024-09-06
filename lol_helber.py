import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import time

class ImageApp:
    def __init__(self, root, image_path):
        self.root = root
        self.image_path = image_path
        self.original_image = Image.open(image_path)
        self.current_image = self.original_image
        self.tk_image = ImageTk.PhotoImage(self.current_image)

        # 이미지와 타이머 레이블을 설정
        self.image_label = tk.Label(root, image=self.tk_image)
        self.image_label.pack()
        
        self.timer_label = tk.Label(root, text="", font=("Arial", 16), bg="white")
        self.timer_label.pack()
        
        self.image_label.bind("<Button-1>", self.on_image_click)
        
        self.remaining_time = 0

    def on_image_click(self, event):
        # 회색 이미지로 변환
        gray_image = ImageOps.grayscale(self.original_image).convert("RGB")
        self.current_image = gray_image
        self.tk_image = ImageTk.PhotoImage(self.current_image)
        self.image_label.config(image=self.tk_image)

        # 타이머 설정 (5분 = 300초)
        self.remaining_time = 300
        self.update_timer()
        self.root.after(1000, self.countdown)  # 매 초마다 타이머 업데이트

    def update_timer(self):
        minutes, seconds = divmod(self.remaining_time, 60)
        self.timer_label.config(text=f"Time remaining: {minutes:02}:{seconds:02}")

    def countdown(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_timer()
            self.root.after(1000, self.countdown)  # 1초 후에 다시 호출
        else:
            # 타이머 종료 시 원래 이미지로 복원
            self.restore_image()

    def restore_image(self):
        # 원래 이미지로 복원
        self.current_image = self.original_image
        self.tk_image = ImageTk.PhotoImage(self.current_image)
        self.image_label.config(image=self.tk_image)
        self.timer_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Image Click Example")
    app = ImageApp(root, './spell_img/barrier.webp')  # 'example.jpg'을 사용자의 이미지 파일로 변경하세요
    root.mainloop()
import tkinter as tk
from PIL import Image, ImageTk, ImageOps

# 각 스펠의 기본 쿨타임 (단위: 초)
SPELL_COOLDOWNS = {
    "베리어": 180, "정화": 210, "총명": 240, "탈진": 180, "점멸": 300,
    "점화": 180, "강타": 15, "텔레포트": 360, "유체화": 210, "회복": 240
}

# 스펠 이미지 파일 경로 (.webp 확장자 사용)
SPELL_IMAGES = {
    "베리어": "./spell_img/barrier.webp",
    "정화": "./spell_img/cleanse.webp",
    "총명": "./spell_img/clarity.webp",
    "탈진": "./spell_img/exhaust.webp",
    "점멸": "./spell_img/flash.webp",
    "점화": "./spell_img/ignite.webp",
    "강타": "./spell_img/smite.webp",   
    "텔레포트": "./spell_img/teleport.webp",
    "유체화": "./spell_img/ghost.webp",
    "회복": "./spell_img/heal.webp"
}

class SpellCooldownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("롤 스펠 계산기")

        # 각 라인을 위한 스펠 이미지 선택 및 이미지 레이블 생성
        self.lines = ["탑", "정글", "미드", "원딜", "서폿"]
        self.spell_selection = {}
        self.spell_images = {}

        # 스펠 이미지 클릭을 위한 상태 관리
        self.selected_spells = {line: [] for line in self.lines}
        self.spell_labels = {}

        # 각 라인별로 스펠 선택 영역 설정
        for idx, line in enumerate(self.lines):
            # 라인 레이블
            line_label = tk.Label(root, text=f"{line} |", font=("Arial", 14))
            line_label.grid(row=idx, column=0, padx=10, pady=10)

            # 각 라인별로 스펠 이미지 레이블 두 개 배치
            spell1_image_label = tk.Label(root)
            spell2_image_label = tk.Label(root)
            spell1_image_label.grid(row=idx, column=1, padx=5, pady=10)
            spell2_image_label.grid(row=idx, column=2, padx=5, pady=10)

            # 타이머 공간 확보를 위한 빈 레이블 추가
            timer_placeholder1 = tk.Label(root, text="", font=("Arial", 14))
            timer_placeholder2 = tk.Label(root, text="", font=("Arial", 14))
            timer_placeholder1.grid(row=idx + 1, column=1)
            timer_placeholder2.grid(row=idx + 1, column=2)

            self.spell_images[line] = (spell1_image_label, spell2_image_label)

        # 모든 스펠 이미지 표시
        self.display_spell_pool()

    def display_spell_pool(self):
        # 전체 스펠 풀을 화면 하단에 표시
        row = len(self.lines) + 2
        col = 0

        for spell_name, image_path in SPELL_IMAGES.items():
            # 스펠 이미지 로드 및 레이블 생성
            image = Image.open(image_path)
            image = image.resize((50, 50), Image.Resampling.LANCZOS)
            tk_image = ImageTk.PhotoImage(image)

            spell_label = tk.Label(self.root, image=tk_image)
            spell_label.grid(row=row, column=col, padx=5, pady=5)
            spell_label.image = tk_image

            # 스펠 클릭 시 선택 함수 실행 (좌클릭)
            spell_label.bind("<Button-1>", lambda e, spell_name=spell_name: self.select_spell(spell_name))

            self.spell_labels[spell_name] = spell_label
            col += 1
            if col > 4:
                col = 0
                row += 1

    def select_spell(self, spell_name):
        # 스펠 선택 시 클릭된 스펠을 라인에 할당
        for line in self.lines:
            if len(self.selected_spells[line]) < 2:  # 각 라인은 2개 스펠만 선택 가능
                self.selected_spells[line].append(spell_name)
                self.update_selected_spells(line)
                return

    def update_selected_spells(self, line):
        # 각 라인의 스펠 이미지를 업데이트
        spell_labels = self.spell_images[line]
        for i, spell_name in enumerate(self.selected_spells[line]):
            if i < 2:  # 스펠이 두 개까지만 선택되므로
                spell_image_path = SPELL_IMAGES.get(spell_name)
                self.display_spell_image(spell_labels[i], spell_image_path, SPELL_COOLDOWNS[spell_name], line, spell_name)

    def display_spell_image(self, label, image_path, cooldown, line, spell_name):
        # 이미지를 라벨에 표시
        image = Image.open(image_path)
        image = image.resize((50, 50), Image.Resampling.LANCZOS)
        tk_image = ImageTk.PhotoImage(image)
        label.config(image=tk_image)
        label.image = tk_image
        label.cooldown_active = False  # 쿨타임 상태를 추적
        label.is_gray = False  # 이미지를 회색 상태로 초기화
        
        # 좌클릭 이벤트 바인딩 (스펠 쿨타임 처리)
        label.bind("<Button-1>", lambda e: self.start_cooldown(label, image_path, cooldown))
        # 우클릭 이벤트 바인딩 (스펠 삭제 처리)
        label.bind("<Button-3>", lambda e: self.remove_spell(label, line, spell_name))

    def remove_spell(self, label, line, spell_name):
        # 우클릭 시 스펠을 제거하고 초기화
        if spell_name in self.selected_spells[line]:
            self.selected_spells[line].remove(spell_name)  # 선택한 스펠 목록에서 제거

            # 쿨타임이 활성 상태일 경우 타이머를 제거
            if label.cooldown_active:
                label.cooldown_active = False
                if hasattr(label, "timer_label"):
                    label.timer_label.destroy()  # 타이머 레이블 제거

            label.config(image="")  # 이미지 제거
            label.unbind("<Button-1>")  # 좌클릭 이벤트 제거
            label.unbind("<Button-3>")  # 우클릭 이벤트 제거

    def start_cooldown(self, label, image_path, cooldown):
        # 클릭 시 회색 이미지로 변경 및 타이머 시작
        if not label.is_gray:  # 회색 상태일 때는 클릭 무시
            original_image = Image.open(image_path)
            gray_image = ImageOps.grayscale(original_image).convert("RGB")
            gray_image = gray_image.resize((50, 50), Image.Resampling.LANCZOS)
            tk_gray_image = ImageTk.PhotoImage(gray_image)
            label.config(image=tk_gray_image)
            label.image = tk_gray_image
            label.is_gray = True
            label.cooldown_active = True  # 쿨타임 상태를 추적

            # 타이머 레이블 생성 (검은색 글씨)
            label.timer_label = tk.Label(self.root, text=f"{cooldown}s", fg="black", font=("Arial", 14))
            label.timer_label.place(x=label.winfo_x(), y=label.winfo_y() + 50)

            # 쿨타임 후 원래 이미지 복원
            self.cooldown_timer(cooldown, label, original_image)

    def cooldown_timer(self, remaining_time, label, original_image):
        if remaining_time > 0 and label.cooldown_active:  # 쿨타임이 활성 상태일 경우만 타이머를 업데이트
            label.timer_label.config(text=f"{remaining_time}s")
            self.root.after(1000, self.cooldown_timer, remaining_time - 1, label, original_image)
        else:
            if label.cooldown_active:  # 쿨타임이 끝났을 때만 이미지 복원
                # 원래 이미지로 복원
                tk_original_image = ImageTk.PhotoImage(original_image.resize((50, 50), Image.Resampling.LANCZOS))
                label.config(image=tk_original_image)
                label.image = tk_original_image
                label.is_gray = False  # 다시 클릭 가능하게 상태 변경
                label.cooldown_active = False
                label.timer_label.destroy()  # 타이머 레이블 삭제

if __name__ == "__main__":
    root = tk.Tk()
    app = SpellCooldownApp(root)
    root.mainloop()
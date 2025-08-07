import customtkinter as ctk
from app import config
from datetime import datetime
import tkinter.messagebox as msgbox
import subprocess
import sys
import os

def resource_path(relative_path):
    """取得資源檔案的絕對路徑，EXE 打包後會指到執行檔的所在資料夾"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(os.path.dirname(sys.executable), relative_path) if getattr(sys, 'frozen', False) else os.path.join(base_path, relative_path)

# 備份資料夾路徑
BACKUP_DIR = resource_path('backups')
os.makedirs(BACKUP_DIR, exist_ok=True)

class ChatBackupApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("阿猴&金蕉 對話備份工具 Pro 版")
        self.geometry("850x760")

        # 載入分類
        self.categories = config.load_categories()
        self.category_var = ctk.StringVar(value=self.categories[0] if self.categories else "")

        # ===== 對話輸入區 =====
        self.label = ctk.CTkLabel(self, text="請貼上 ChatGPT 對話內容：", font=("微軟正黑體", 20))
        self.label.pack(pady=(20, 10))

        self.text_area = ctk.CTkTextbox(self, width=700, height=350, font=("微軟正黑體", 16), corner_radius=10)
        self.text_area.pack(pady=10)

        # ===== 分類選單 =====
        self.category_label = ctk.CTkLabel(self, text="選擇分類：", font=("微軟正黑體", 20))
        self.category_label.pack(pady=(20, 10))

        self.category_menu = ctk.CTkOptionMenu(self, variable=self.category_var, values=self.categories, font=("微軟正黑體", 16), width=200)
        self.category_menu.pack(pady=10)

        # ===== 儲存按鈕 =====
        self.save_button = ctk.CTkButton(self, text="儲存對話", font=("微軟正黑體", 18), command=self.save_chat)
        self.save_button.pack(pady=(30, 15), ipadx=20, ipady=10)

        # ===== 分類管理區 =====
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        self.add_button = ctk.CTkButton(
            button_frame,
            text="新增分類",
            font=("微軟正黑體", 18),
            fg_color="#007500",  # 綠色
            hover_color="#006000",
            text_color="white",
            command=self.add_category
        )
        self.add_button.pack(side="left", padx=10, ipadx=20, ipady=10)

        # 修改分類 → 紫色
        self.edit_button = ctk.CTkButton(
            button_frame,
            text="修改分類",
            font=("微軟正黑體", 18),
            fg_color="#9C27B0",  # 紫色
            hover_color="#7B1FA2",  # 滑鼠移過變深紫
            text_color="white",
            command=self.edit_category
        )
        self.edit_button.pack(side="left", padx=10, ipadx=20, ipady=10)

        # 刪除分類 → 紅色
        self.delete_button = ctk.CTkButton(
            button_frame,
            text="刪除分類",
            font=("微軟正黑體", 18),
            fg_color="#F44336",  # 紅色
            hover_color="#D32F2F",  # 滑鼠移過變深紅
            text_color="white",
            command=self.delete_category
        )
        self.delete_button.pack(side="left", padx=10, ipadx=20, ipady=10)

        # 打開備份資料夾 → 藍色
        self.open_folder_button = ctk.CTkButton(
            button_frame,
            text="📂 打開備份資料夾",
            font=("微軟正黑體", 18),
            fg_color="#EA7500",
            hover_color="#D26900",
            text_color="white",
            command=lambda: self.open_folder(BACKUP_DIR)  # 這裡包一個函式呼叫帶參數
        )
        self.open_folder_button.pack(side="left", padx=10, ipadx=20, ipady=10)

        # 在 UI 上加這顆按鈕
        self.theme_button = ctk.CTkButton(self, text="切換白天/夜晚模式", font=("微軟正黑體", 18),
                                          command=self.toggle_theme)
        self.theme_button.pack(padx=10, ipadx=20, ipady=10)

    def save_chat(self):
        content = self.text_area.get("1.0", "end").strip()
        category = self.category_var.get()

        if not content:
            print("⚠️ 對話內容是空的，不儲存。")
            msgbox.showwarning("儲存失敗", "⚠️ 對話內容是空的，無法儲存。")
            return

        if not category:
            print("⚠️ 沒有選擇分類，不儲存。")
            msgbox.showwarning("儲存失敗", "⚠️ 請先選擇分類，才能儲存。")
            return

        # 確保分類資料夾存在
        category_dir = os.path.join(BACKUP_DIR, category)
        os.makedirs(category_dir, exist_ok=True)

        # 檔名用日期＋時間
        timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        filename = f"{timestamp}.txt"
        file_path = os.path.join(category_dir, filename)

        # 儲存對話內容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ 對話已儲存到 {file_path}")

        # 視窗提示成功
        msgbox.showinfo("備份完成", f"📦 備份好了唷～\n分類：{category}\n檔案位置：\n{file_path}")

        self.open_folder(category_dir)

    # 👉 打開資料夾函式
    def open_folder(self, path):
        if os.path.exists(path):
            try:
                subprocess.Popen(f'explorer "{path}"')  # Windows only
            except Exception as e:
                msgbox.showerror("錯誤", f"無法開啟資料夾：\n{e}")
        else:
            msgbox.showwarning("找不到資料夾", "指定的資料夾不存在。")

    def add_category(self):
        new_cat = ctk.CTkInputDialog(text="請輸入新分類名稱：", title="新增分類").get_input()
        if new_cat:
            self.categories.append(new_cat)
            config.save_categories(self.categories)  # ← 寫入設定檔
            self.category_menu.configure(values=self.categories)
            self.category_var.set(new_cat)

    def edit_category(self):
        current_cat = self.category_var.get()
        if not current_cat:
            return
        new_cat = ctk.CTkInputDialog(text=f"將「{current_cat}」修改為：", title="修改分類").get_input()
        if new_cat:
            index = self.categories.index(current_cat)
            self.categories[index] = new_cat
            config.save_categories(self.categories)
            self.category_menu.configure(values=self.categories)
            self.category_var.set(new_cat)

    def delete_category(self):
        current_cat = self.category_var.get()
        if current_cat and current_cat in self.categories:
            self.categories.remove(current_cat)
            config.save_categories(self.categories)
            self.category_menu.configure(values=self.categories)
            if self.categories:
                self.category_var.set(self.categories[0])
            else:
                self.category_var.set("")

    def toggle_theme(self):
        current_mode = ctk.get_appearance_mode().lower()
        new_mode = "dark" if current_mode == "light" else "light"
        ctk.set_appearance_mode(new_mode)
        self.theme_button.configure(text=f"切換到 {'白天' if new_mode == 'dark' else '夜晚'} 模式")

if __name__ == "__main__":
    app = ChatBackupApp()
    app.mainloop()

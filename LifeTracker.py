import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
from datetime import datetime, timedelta
from fpdf import FPDF
import matplotlib.pyplot as plt
import webbrowser

DATA_DIR = "data"
REPORTS_DIR = "reports"
FONT_PATH = "DejaVuSans.ttf"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

class LifeTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Burak's Life Tracker")
        self.root.geometry("1200x700")
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.data = self.load_data()

        self.setup_style()
        self.create_widgets()

    def setup_style(self):
        style = ttk.Style()
        self.root.configure(bg='SystemButtonFace')
        style.theme_use('clam')
        style.configure("TLabel", background="SystemButtonFace", foreground="black")
        style.configure("TButton", background="SystemButtonFace", foreground="black")
        style.configure("TFrame", background="SystemButtonFace")
        style.configure("TEntry", fieldbackground="white", foreground="black")

    def create_widgets(self):
        top_frame = ttk.Frame(self.root)
        top_frame.pack(pady=10)
        ttk.Button(top_frame, text="Bugünü Kaydet", command=self.save_day_data).pack(side='left', padx=5)
        ttk.Button(top_frame, text="Aylık Raporu Oluştur", command=self.generate_monthly_report).pack(side='left', padx=5)

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(main_frame)
        self.scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="left", fill="y")

        self.entries = {}
        self.create_form()

        self.calendar_canvas = tk.Canvas(main_frame, width=300, height=300, bg='white', highlightthickness=1, highlightbackground="gray")
        self.calendar_canvas.pack(side="right", padx=10, pady=10)
        self.draw_calendar()

    def create_form(self):
        questions = [
            ("mood", "Bugünkü ruh halini 1-10 arası puanla:"),
            ("journal", "Bugün seni en çok etkileyen şey neydi?"),
            ("reading", "Kaç sayfa kitap okudun?"),
            ("book", "Hangi kitabı okudun?"),
            ("sleep", "Kaç saat uyudun?"),
            ("water", "Kaç litre su içtin?"),
            ("steps", "Kaç adım attın?"),
            ("workout", "Hangi antrenmanı yaptın?"),
            ("programming", "Kaç dakika kod yazdın?"),
            ("project", "Ne geliştirdin ya da ne öğrendin?"),
            ("diet", "Diyetine sadık kaldın mı?"),
            ("vitamins", "Vitamin takviyesi aldın mı?"),
            ("alone", "Kendinle baş başa kaç dakika geçirdin?"),
            ("music", "Bugün dinlediğin şarkılar nelerdi?")
        ]
        for key, label in questions:
            ttk.Label(self.scrollable_frame, text=label).pack(anchor='w', pady=2)
            entry = tk.Text(self.scrollable_frame, height=2, width=110)
            entry.pack(pady=2)
            self.entries[key] = entry

    def save_day_data(self):
        if self.date in self.data:
            messagebox.showwarning("Uyarı", f"{self.date} için zaten veri girildi.")
            return

        day_data = {}
        for key, widget in self.entries.items():
            content = widget.get("1.0", tk.END).strip()
            day_data[key] = content

        self.data[self.date] = day_data
        self.write_data()
        self.draw_calendar()
        messagebox.showinfo("Başarılı", "Bugünün verileri kaydedildi.")

    def load_data(self):
        path = os.path.join(DATA_DIR, f"{datetime.now().strftime('%Y-%m')}.json")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def write_data(self):
        path = os.path.join(DATA_DIR, f"{datetime.now().strftime('%Y-%m')}.json")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def generate_monthly_report(self):
        month = datetime.now().strftime('%Y-%m')
        data_file = os.path.join(DATA_DIR, f"{month}.json")
        if not os.path.exists(data_file):
            messagebox.showerror("Hata", "Bu ay için veri bulunamadı.")
            return

        with open(data_file, 'r', encoding='utf-8') as f:
            month_data = json.load(f)

        def safe_int(value):
            try:
                return int(value.strip())
            except:
                return 0

        total_pages = sum(safe_int(entry.get("reading", "0")) for entry in month_data.values())
        total_coding = sum(safe_int(entry.get("programming", "0")) for entry in month_data.values())
        total_steps = sum(safe_int(entry.get("steps", "0")) for entry in month_data.values())
        mood_scores = [safe_int(entry.get("mood", "0")) for entry in month_data.values() if entry.get("mood")]
        avg_mood = sum(mood_scores) / len(mood_scores) if mood_scores else 0

        motivasyon = [
            "Kendine biraz zaman tanı. Her gün aynı olmayabilir, bu da çok insanca.",
            "Zorluklar seni durdurmasın. Yavaş ama sağlam ilerliyorsun.",
            "Yılmadığın sürece hiçbir şey bitmiş sayılmaz.",
            "Küçük başarılar, büyük değişimlerin habercisidir.",
            "Dengeyi korumak bir başarıdır. Azı da iyidir.",
            "Fena değil! Biraz daha odakla çok şey değişebilir.",
            "Gayet iyisin! Kendini küçümseme.",
            "Sen bu ay ciddi yol katetmişsin. Aferin sana!",
            "Harika! Disiplinin etkisi hissediliyor.",
            "Muhteşemsin. Bu seviyeyi koru, sen örnek oluyorsun.",
            "İnanılmaz bir ay geçirmişsin! Resmen ilham kaynağısın."
        ]
        moral_comment = motivasyon[round(avg_mood)]

        days = list(month_data.keys())
        coding = [safe_int(month_data[day].get("programming", 0)) for day in days]

        plt.figure(figsize=(10, 5))
        plt.bar(days, coding, color='teal')
        plt.xticks(rotation=45)
        plt.title("Kodlama Süresi (dk)")
        plt.tight_layout()
        chart_path = os.path.join(REPORTS_DIR, f"{month}-chart.png")
        plt.savefig(chart_path)
        plt.close()

        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('DejaVu', '', FONT_PATH, uni=True)
        pdf.set_font("DejaVu", size=12)
        pdf.cell(200, 10, txt=f"Burak Aylık Rapor - {month}", ln=True, align='C')
        pdf.ln(10)
        content = f"Toplam okunan sayfa: {total_pages}\n" \
                  f"Toplam kodlama süresi: {total_coding} dk\n" \
                  f"Toplam adım: {total_steps}\n" \
                  f"Ortalama moral puanı: {avg_mood:.1f}/10\n" \
                  f"Motivasyon: {moral_comment}"
        pdf.multi_cell(0, 10, content)
        pdf.image(chart_path, x=10, y=None, w=180)

        pdf_path = os.path.join(REPORTS_DIR, f"{month}-report.pdf")
        pdf.output(pdf_path)
        webbrowser.open_new(pdf_path)
        messagebox.showinfo("Rapor Oluşturuldu", f"Rapor başarıyla kaydedildi: {pdf_path}")

    def draw_calendar(self):
        self.calendar_canvas.delete("all")
        today = datetime.now().date()
        year, month = today.year, today.month
        first_day = datetime(year, month, 1).date()
        start_day = first_day.weekday()
        cell_size = 40

        for i in range(31):
            current = first_day + timedelta(days=i)
            if current.month != month:
                break
            row = (start_day + i) // 7
            col = (start_day + i) % 7
            x0 = col * cell_size
            y0 = row * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size

            date_str = current.strftime("%Y-%m-%d")
            file_path = os.path.join(DATA_DIR, f"{current.strftime('%Y-%m')}.json")
            exists = False

            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    month_data = json.load(f)
                    exists = date_str in month_data

            if current > today:
                color, symbol = "red", "X"
            elif exists:
                color, symbol = "green", "✓"
            else:
                color, symbol = "orange", "?"

            self.calendar_canvas.create_rectangle(x0, y0, x1, y1, fill=color)
            self.calendar_canvas.create_text((x0+x1)//2, (y0+y1)//2, text=str(current.day), fill="white")
            self.calendar_canvas.create_text((x0+x1)//2, y1-5, text=symbol, fill="white", font=("Arial", 8))

if __name__ == "__main__":
    root = tk.Tk()
    app = LifeTrackerApp(root)
    root.mainloop()

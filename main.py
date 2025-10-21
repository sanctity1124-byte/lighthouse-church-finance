
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from fpdf import FPDF
import os

APP_TITLE = "등대교회 재정관리"
DB_DIR = os.path.join(os.path.expanduser("~"), "Documents", "등대교회_재정관리")
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR, exist_ok=True)

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("820x600")
        self.data = pd.DataFrame(columns=["날짜", "구분", "항목", "금액", "비고"])
        self.build_ui()

    def build_ui(self):
        frm = ttk.Frame(self.root, padding=12)
        frm.pack(fill="both", expand=True)

        top = ttk.Frame(frm)
        top.pack(fill="x", pady=6)
        ttk.Label(top, text="구분:").grid(row=0, column=0, sticky="w")
        self.type_var = tk.StringVar(value="수입")
        ttk.Combobox(top, textvariable=self.type_var, values=["수입","지출"], width=10).grid(row=0, column=1, padx=6)
        ttk.Label(top, text="항목:").grid(row=0, column=2, sticky="w")
        self.item_var = tk.Entry(top, width=20); self.item_var.grid(row=0, column=3, padx=6)
        ttk.Label(top, text="금액:").grid(row=0, column=4, sticky="w")
        self.amount_var = tk.Entry(top, width=12); self.amount_var.grid(row=0, column=5, padx=6)
        ttk.Label(top, text="비고:").grid(row=0, column=6, sticky="w")
        self.note_var = tk.Entry(top, width=20); self.note_var.grid(row=0, column=7, padx=6)

        btns = ttk.Frame(frm); btns.pack(fill="x", pady=6)
        ttk.Button(btns, text="추가", command=self.add_entry).pack(side="left", padx=4)
        ttk.Button(btns, text="엑셀로 저장", command=self.save_excel).pack(side="left", padx=4)
        ttk.Button(btns, text="PDF로 저장", command=self.save_pdf).pack(side="left", padx=4)
        ttk.Button(btns, text="불러오기(CSV)", command=self.load_csv).pack(side="left", padx=4)
        ttk.Button(btns, text="합계 보기", command=self.show_summary).pack(side="left", padx=4)

        table_frm = ttk.Frame(frm); table_frm.pack(fill="both", expand=True)
        cols = ["날짜","구분","항목","금액","비고"]
        self.tree = ttk.Treeview(table_frm, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="w", width=140 if c!='금액' else 100)
        vsb = ttk.Scrollbar(table_frm, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

    def add_entry(self):
        try:
            amt = int(self.amount_var.get())
        except:
            messagebox.showwarning("입력 오류", "금액은 숫자만 입력하세요.")
            return
        entry = {
            "날짜": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            "구분": self.type_var.get(),
            "항목": self.item_var.get(),
            "금액": amt,
            "비고": self.note_var.get()
        }
        self.data = pd.concat([self.data, pd.DataFrame([entry])], ignore_index=True)
        self.tree.insert("", "end", values=(entry["날짜"], entry["구분"], entry["항목"], f"{entry['금액']:,}", entry["비고"]))
        self.item_var.delete(0, tk.END); self.amount_var.delete(0, tk.END); self.note_var.delete(0, tk.END)

    def save_excel(self):
        path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel","*.xlsx")])
        if not path: return
        self.data.to_excel(path, index=False)
        messagebox.showinfo("저장 완료", f"엑셀 파일이 저장되었습니다:\n{path}")

    def save_pdf(self):
        path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF","*.pdf")])
        if not path: return
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=11)
        pdf.cell(200, 10, txt="등대교회 재정관리 내역", ln=True, align="C")
        pdf.ln(6)
        for _, r in self.data.iterrows():
            pdf.cell(0, 8, txt=f"{r['날짜']} | {r['구분']} | {r['항목']} | {r['금액']} | {r['비고']}", ln=True)
        pdf.output(path)
        messagebox.showinfo("PDF 저장", f"PDF가 저장되었습니다:\n{path}")

    def load_csv(self):
        p = filedialog.askopenfilename(filetypes=[("CSV","*.csv"),("All","*.*")])
        if not p: return
        try:
            df = pd.read_csv(p)
            for _, r in df.iterrows():
                self.tree.insert("", "end", values=(r.get("날짜",""), r.get("구분",""), r.get("항목",""), f"{int(r.get('금액',0)):,}", r.get("비고","")))
            messagebox.showinfo("불러오기", "CSV 불러오기 완료")
        except Exception as e:
            messagebox.showerror("오류", str(e))

    def show_summary(self):
        income = self.data[self.data["구분"]=="수입"]["금액"].sum()
        expense = self.data[self.data["구분"]=="지출"]["금액"].sum()
        messagebox.showinfo("요약", f"총 수입: {income:,}원\n총 지출: {expense:,}원\n잔액: {income-expense:,}원")

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()

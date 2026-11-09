import json,csv,time,threading,queue,os
from pathlib import Path
import tkinter as tk
from tkinter import ttk,filedialog,messagebox
from job_sources import search_jobs
from apply_runner import apply_job
ROOT=Path(__file__).parent; PF=ROOT/"profile.json"; HIST=ROOT/"applications.csv"
def loadp():
 try:return json.loads(PF.read_text())
 except:return json.loads((ROOT/"profile.example.json").read_text())
class App:
 def __init__(self,r):
  self.r=r;r.title("SkyJob AutoApply");r.geometry("950x650");self.p=loadp();self.q=queue.Queue();self.stop=threading.Event()
  f=ttk.Frame(r,padding=15);f.pack(fill="both",expand=True)
  ttk.Label(f,text="SkyJob AutoApply",font=("Segoe UI",20,"bold")).pack(anchor="w")
  ttk.Label(f,text="Mumbai • 2–3 YOE • job search & application assistance").pack(anchor="w",pady=5)
  g=ttk.LabelFrame(f,text="Candidate profile",padding=8);g.pack(fill="x")
  self.entries={}
  for label,key in [("Name","name"),("Email","email"),("Phone","phone"),("Resume PDF path","resume_path"),("Locations (comma separated)","locations"),("Job titles (comma separated)","keywords")]:
   row=ttk.Frame(g);row.pack(fill="x",pady=3);ttk.Label(row,text=label,width=25).pack(side="left")
   val=self.p.get(key,"");val=", ".join(val) if isinstance(val,list) else val
   e=ttk.Entry(row);e.insert(0,val);e.pack(side="left",fill="x",expand=True);self.entries[key]=e
   if key=="resume_path":ttk.Button(row,text="Browse",command=lambda:self.browse()).pack(side="right")
  bar=ttk.Frame(f);bar.pack(fill="x",pady=8);ttk.Button(bar,text="Save Profile",command=self.save).pack(side="left");self.start=ttk.Button(bar,text="SEARCH & ASSIST APPLY",command=self.run);self.start.pack(side="left",padx=8)
  self.status=tk.StringVar(value="Ready");ttk.Label(f,textvariable=self.status).pack(anchor="w")
  self.tree=ttk.Treeview(f,columns=("title","company","location","source","status"),show="headings",height=16)
  for c,w in [("title",280),("company",150),("location",140),("source",100),("status",150)]:self.tree.heading(c,text=c.title());self.tree.column(c,width=w)
  self.tree.pack(fill="both",expand=True,pady=5)
  ttk.Label(f,text="Review each opened page and click Submit yourself. CAPTCHA/OTP are not bypassed.",wraplength=900).pack(anchor="w")
  self.poll()
 def browse(self):
  x=filedialog.askopenfilename(filetypes=[("PDF","*.pdf")])
  if x:self.entries["resume_path"].delete(0,"end");self.entries["resume_path"].insert(0,x)
 def save(self):
  p={k:e.get() for k,e in self.entries.items()};p["locations"]=[x.strip() for x in p["locations"].split(",") if x.strip()];p["keywords"]=[x.strip() for x in p["keywords"].split(",") if x.strip()]
  PF.write_text(json.dumps(p,indent=2));self.p=p;self.status.set("Profile saved (private profile.json is gitignored).")
 def run(self):
  self.save();self.start.configure(state="disabled");self.status.set("Searching configured boards…");threading.Thread(target=self.worker,daemon=True).start()
 def worker(self):
  try:
   jobs=search_jobs(self.p,self.stop);self.q.put(("found",jobs))
   for j in jobs:
    if self.stop.is_set():break
    self.q.put(("res",j,apply_job(j,self.p)));time.sleep(1)
   self.q.put(("done",len(jobs)))
  except Exception as e:self.q.put(("err",str(e)))
 def poll(self):
  try:
   while True:
    a=self.q.get_nowait()
    if a[0]=="found":
     for j in a[1]:self.tree.insert("","end",values=(j["title"],j["company"],j["location"],j["source"],"Found"))
     self.status.set(f"Found {len(a[1])} jobs. Opening each for review.")
    elif a[0]=="res":
     j,s=a[1],a[2]
     for iid in self.tree.get_children():
      v=self.tree.item(iid,"values")
      if v[0]==j["title"] and v[1]==j["company"]:self.tree.set(iid,"status",s);break
     with HIST.open("a",newline="",encoding="utf-8") as h:csv.writer(h).writerow([time.strftime("%Y-%m-%d %H:%M"),j["title"],j["company"],j["location"],j["url"],s])
    elif a[0]=="done":self.status.set(f"Done: {a[1]} job pages processed. See applications.csv.");self.start.configure(state="normal")
    elif a[0]=="err":self.status.set("Error: "+a[1]);self.start.configure(state="normal")
  except queue.Empty:pass
  self.r.after(250,self.poll)
if __name__=="__main__":r=tk.Tk();App(r);r.mainloop()

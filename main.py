from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
from socket import *
from requests import *
from bs4 import *
from pandas import *
import matplotlib.pyplot as plt
from numpy import *


def f1():
	Adst.deiconify()
	root.withdraw()
	
def f2():
	root.deiconify()
	Adst.withdraw()
	Viewst.withdraw()
	Upst.withdraw()
	Delst.withdraw()

def f3():
	Viewst.deiconify()
	root.withdraw()
	Viewst_data.delete(1.0,END)
	con=None
	try:	
		con=connect("project.db")
		cursor=con.cursor()
		sql="select * from student"
		cursor.execute(sql)
		info=cursor.fetchall()
		msg=""
		for i in info:
			msg=str(i[0]) + " " +str(i[1]) + " " + str(i[2]) + "\n"

			Viewst_data.insert(INSERT,msg)
	except Exception as e:
		showerror("Issue", e)
	finally:
		if con is not None:
			con.close()
	
	
def f4():
	Upst.deiconify()
	root.withdraw()

def f5():
	Delst.deiconify()
	root.withdraw()

def add():
	
	con=None
	rno=""
	try:
		con=connect("project.db")
		rno=int(Adstrno_ent.get())
		name=Adstname_ent.get()
		marks=int(Adstmarks_ent.get())

		if (rno<=0) :
			showerror("Error" ,"Rno cannot be 0 or negative number.")

		elif (len(name)<2 or (not name.isalpha())):
			showerror("Error","Name should contain only letters with length above 2 characters.")
		elif (marks<0 or marks>100):
			showerror("Error","Marks should be +ve and in range 0 to 100.")
		else:	
			cursor=con.cursor()
			sql="insert into student values( '%d' , '%s' , '%d')"
			cursor.execute(sql % (rno , name , marks))
			con.commit()
			showinfo("Add St.", "Record added.")
	except ValueError:
			con.rollback()
			showerror("Value Error"," Check the values entered.")
			Adstrno_ent.focus()

	except Exception as e:			
			con.rollback()
			showerror("Issue",e)
			Adstrno_ent.focus()
	finally:
		if con is not None:
			con.close()
			Adstrno_ent.delete(0,END)
			Adstname_ent.delete(0,END)
			Adstmarks_ent.delete(0,END)
			Adstrno_ent.focus()
			
def update():
	con = None
	try:
		con = connect("project.db")
		cursor=con.cursor()
		rno=int(Upstrno_ent.get())
		name=Upstname_ent.get()
		marks=int(Upstmarks_ent.get())
		if rno<0 :
			showerror("Rno_Error","Value has to be +ve and greater than 0.") 
		elif (len(name)<2 or (not name.isalpha())):
			showerror("Name_Error","Name should contain only letters with length above 2 characters. ")
		elif(marks<0 or marks>100):
			showerror("Marks_Error","Marks should be in range 0 to 100.")

		else:
			sql="update student set name='%s', marks='%d' where rno='%d' "
			cursor.execute(sql %( name, marks, rno))
			if cursor.rowcount>0:
				con.commit()
				showinfo("Success","Record updated.")
			else:
				showinfo("OOPS","Record doesn't exist.")
				Upstrno_ent.focus()			

	except ValueError:
		showerror("ValueError","Check the entered values.")	

	except Exception as e:
		con.rollback()
		showerror("Error",e)
		Upstrno_ent.focus()

	finally:
		if con is not None:
			con.close()
			Upstrno_ent.delete(0,END)
			Upstname_ent.delete(0,END)
			Upstmarks_ent.delete(0,END)
			Upstrno_ent.focus()	
def remove():
	con=None
	try:
		con=connect("project.db")
		cursor=con.cursor()
		rno=int(Delstrno_ent.get())
		if rno<0:
			showerror("Error","rno has to be a positive number.")
		sql="delete from student where rno ='%d'"
		cursor.execute(sql % (rno))
		if cursor.rowcount>0:
			showinfo("Success","Record deleted.")
		else:
			showinfo("OOPS","Record doesn't exist. ")
		

		con.commit()
	
	except ValueError:
		showerror("Value Error","Check the values entered.")
			
	except Exception as e:
		con.rollback()
		showerror("Issue",e)
		Delstrno_ent.delete(1.0,END)	
		
		
	finally:
		if con is not None:
			con.close()
			Delstrno_ent.delete(0,END)

def charts():
	data=read_csv("chart_data.csv")
	rno=data['rno'].tolist()
	name=data['name'].tolist()
	marks=data['marks'].tolist()
	
	plt.bar(name, marks, width=0.65, label='Marks')
	plt.legend()
	plt.title("Student Marks")
	plt.xlabel("Names")
	plt.ylabel("Marks")
	plt.grid()
	plt.show()	
	
			
root =Tk()
root.title("S.M.S.")
root.geometry("500x500+400+200")
root.configure(background="#e4f0db")
root.resizable(False,False)

try:
		web_address1="https://ipinfo.io"
		response1=get(web_address1)
		d1=response1.json()
		loc = d1['city']
		

		a1="https://api.openweathermap.org/data/2.5/weather?units=metric"
		a2="&q=mumbai"
		a3="&appid=c6e315d09197cec231495138183954bd"
		web_address2=a1+a2+a3
		response2=get(web_address2)
		d2=response2.json()
		temp=str(d2['main']['temp'])

		web_address3="https://www.brainyquote.com/quote_of_the_day/"
		response3=get(web_address3)
		soup=BeautifulSoup(response3.text,"html.parser")
		tag=soup.find("img",{"class":"p-qotd"})
		quote=tag['alt']
except Exception as e:
		showerror("Error",e)



#var=StringVar()
#var.set(lo)


btnadd=Button(root,text="Add",bd=5,width=7,font=("courier",18,"bold"),command =f1)
btnview = Button(root,text="View",bd=5,width=7,font=("courier",18,"bold"),command=f3)
btnupdate=Button(root,text="Update",bd=5,width=7,font=("courier",18,"bold"),command=f4)
btndel = Button(root,text="Delete",bd=5,width=7,font=("courier",18,"bold"), command=f5)
btncharts=Button(root,text="Charts",bd=5,width=7,font=("courier",18,"bold"),command=charts)
lbl_loc = Label(root,text="Location : "+loc, font=("courier",14,"bold"),background="#e4f0db")
lbl_temp=Label(root,text="Temp : "+temp + ' C',font=("courier",14,"bold"),background="#e4f0db")
lbl_quote=Label(root,text="QOTD: "+quote, font=("courier",14,"bold"),background="#e4f0db",wraplength=500)

btnadd.pack(pady=10)
btnview.pack(pady=10)
btnupdate.pack(pady=10)
btndel.pack(pady=10)
btncharts.pack(pady=10)
lbl_loc.place(x=1, y=370)
lbl_temp.place(x=320,y=370)
#lbl_quote.place(x=1,y=390)
lbl_quote.pack(pady=30)

Adst=Toplevel(root)
Adst.title("Add St.")
Adst.geometry("500x500+400+200")
Adst.configure(background="#dce3f4")

Adstrno_lbl = Label(Adst,text="Enter rno:",font=("courier",18,"bold"),background="#dce3f4")
Adstrno_ent = Entry(Adst,bd=5,font=("courier",18,"bold"))
Adstname_lbl =Label(Adst,text="Enter name:",font=("courier",18,"bold"),background="#dce3f4")
Adstname_ent =Entry(Adst,bd=5,font=("courier",18,"bold"))
Adstmarks_lbl=Label(Adst,text="Enter marks:",font=("courier",16,"bold"),background="#dce3f4")
Adstmarks_ent=Entry(Adst,bd=5,font=("courier",18,"bold"))
Adstsave_btn=Button(Adst,text="Save",font=("courier",18,"bold"),command=add)
Adstback_btn=Button(Adst,text="Back",font=("courier",18,"bold"),command=f2)

Adstrno_lbl.pack(pady=10)
Adstrno_ent.pack(pady=10)
Adstname_lbl.pack(pady=10)
Adstname_ent.pack(pady=10)
Adstmarks_lbl.pack(pady=10)
Adstmarks_ent.pack(pady=10)
Adstsave_btn.pack(pady=10)
Adstback_btn.pack(pady=10)
Adst.withdraw()

Viewst = Toplevel(root)
Viewst.title("View St.")
Viewst.geometry("500x500+500+200")
Viewst.configure(background="#fff3cd")

Viewst_data= ScrolledText(Viewst, width=30,height=10, font=("courier", 18,"bold italic"),background="#fff3cd")
Viewstback_btn=Button(Viewst,text="Back",font=("courier",18,"bold"), command=f2)

Viewst_data.pack()
Viewstback_btn.pack()
Viewst.withdraw()
 
Upst = Toplevel(root)
Upst.title("Update St.")
Upst.geometry("500x500+400+200")
Upst.configure(background="#fce4d7")

Upstrno_lbl = Label(Upst,text="Enter rno:",font=("courier",18,"bold"),background="#fce4d7")
Upstrno_ent = Entry(Upst,bd=5,font=("courier",18,"bold"))
Upstname_lbl =Label(Upst,text="Enter name:",font=("courier",18,"bold"),background="#fce4d7")
Upstname_ent =Entry(Upst,bd=5,font=("courier",18,"bold"))
Upstmarks_lbl=Label(Upst,text="Enter marks:",font=("courier",16,"bold"),background="#fce4d7")
Upstmarks_ent=Entry(Upst,bd=5,font=("courier",18,"bold"))
Upstsave_btn=Button(Upst,text="Save",font=("courier",18,"bold"),command=update)
Upstback_btn=Button(Upst,text="Back",font=("courier",18, "bold"),command=f2)

Upstrno_lbl.pack(pady=10)
Upstrno_ent.pack(pady=10)
Upstname_lbl.pack(pady=10)
Upstname_ent.pack(pady=10)
Upstmarks_lbl.pack(pady=10)
Upstmarks_ent.pack(pady=10)
Upstsave_btn.pack(pady=10)
Upstback_btn.pack(pady=10)
Upst.withdraw()

Delst=Toplevel(root)
Delst.title("Delete St.")
Delst.geometry("500x500+400+200")
Delst.configure(background="#e0eaf8")

Delstrno_lbl=Label(Delst,text="Enter rno:", font=("courier",18,"bold"),background="#e0eaf8")
Delstrno_ent=Entry(Delst,bd=5, font=("courier",18,"bold"))
Delstsave_btn=Button(Delst,text="Save", font=("courier",18,"bold"),command=remove)
Delstback_btn=Button(Delst,text="Back", font=("courier",18,"bold"),command=f2)

Delstrno_lbl.pack(pady=10)
Delstrno_ent.pack(pady=10)
Delstsave_btn.pack(pady=10)
Delstback_btn.pack(pady=10)

Delst.withdraw()

mainloop()
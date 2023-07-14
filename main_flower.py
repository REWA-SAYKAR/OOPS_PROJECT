import customtkinter
import sqlite3
from tkinter import *
from PIL import Image,ImageTk
from tkinter import messagebox
import os
from twilio.rest import Client
from datetime import datetime

app = customtkinter.CTk()
app.title('Pushpamayam')
app.geometry('724x640')
app.config(bg='#000')#diff bet config and configure
app.resizable(False,False)#width and height will not be resizacle if False

font1 = ('Arial',22,'bold')

def get_flowers(): 
    conn = sqlite3.connect('flower.db')
    c = conn.cursor()
    c.execute('SELECT flower_name,price FROM flower')
    results = c.fetchall()
    print(results)
    
    global flower1_details
    global flower2_details
    global flower3_details
    
    flower1_details = results[0]
    flower2_details = results[1]    
    flower3_details = results[2]
    
    p1_name_label.configure(text="{}\nPrice: Rs{}".format(flower1_details[0],flower1_details[1]))
    p2_name_label.configure(text="{}\nPrice: Rs{}".format(flower2_details[0],flower2_details[1]))    
    p3_name_label.configure(text="{}\nPrice: Rs{}".format(flower3_details[0],flower3_details[1]))

    conn.close()
    
def get_quantity():
    conn = sqlite3.connect('flower.db')
    c = conn.cursor()
    c.execute('SELECT quantity FROM flower')
    results = c.fetchall()
    
    global flower1_quantity
    global flower2_quantity
    global flower3_quantity
    
    flower1_quantity = results[0][0]
    flower2_quantity = results[1][0]
    flower3_quantity = results[2][0]

    if flower1_quantity == 0:
        variable1.set('0')
        p1_quatity.destroy()
        p1_state_label = customtkinter.CTkLabel(p1_frame,font=font1,text='Flowers Sold ',text_color='#ff0',bg_color='#000',width=100)
        p1_state_label.place(x=20,y=270)
        
    else:
        list1 = [str(i) for i in range(flower1_quantity+1)]
        p1_quatity.configure(values = list1)
        p1_quatity.set('0')
        
    if flower2_quantity == 0:
        variable2.set('0')
        p2_quatity.destroy()
        p2_state_label = customtkinter.CTkLabel(p2_frame,font=font1,text='Flowers Sold ',text_color='#ff0',bg_color='#000',width=100)
        p2_state_label.place(x=20,y=270)
        
    else:
        list2 = [str(i) for i in range(flower2_quantity+1)]
        p2_quatity.configure(values = list2)
        p2_quatity.set('0')
    
    if flower3_quantity == 0:
        variable3.set('0')
        p3_quatity.destroy()
        p3_state_label = customtkinter.CTkLabel(p3_frame,font=font1,text='Flowers Sold ',text_color='#ff0',bg_color='#000',width=100)
        p3_state_label.place(x=20,y=270)
        
    else:
        list3 = [str(i) for i in range(flower3_quantity+1)]
        p3_quatity.configure(values = list3)
        p3_quatity.set('0')
        

def checkout():
    if flower1_quantity==0 and flower2_quantity==0 and flower3_quantity==0:
        messagebox.showerror('ERROR','Sorry! Out of stock!')
    else:
        if customer_entry.get():
            conn = sqlite3.connect('flower.db')
            c = conn.cursor()
            global qty1
            global qty2 
            global qty3
            qty1 = int(variable1.get())    
            qty2 = int(variable2.get())            
            qty3 = int(variable3.get())
            
            c.execute("UPDATE flower SET quantity = ? WHERE id = ?",(flower1_quantity-qty1,1))
            c.execute("UPDATE flower SET quantity = ? WHERE id = ?",(flower2_quantity-qty2,2))
            c.execute("UPDATE flower SET quantity = ? WHERE id = ?",(flower3_quantity-qty3,3))
            conn.commit()
            conn.close()
            global total_price
            total_price = qty1*flower1_details[1] + qty2*flower2_details[1] + qty3*flower3_details[1]
            if total_price == 0:
                messagebox.showinfo('NOTE','Please choose the flowers')
            else:
                price_label.configure(text=f'Price:Rs{total_price}')
                get_quantity()
                with open('Order_receipts.txt','a') as f:
                    f.write(f'\nName --> {customer_entry.get()}\n')
                    f.write(f'Anemones --> {qty1}\n')
                    f.write(f'White Roses --> {qty2}\n')
                    f.write(f'Tulips --> {qty3}\n')
                    f.write(f'Total BILL --> Rs{total_price}\n')
                    f.write(f'------------------\nThankYou\n------------------')
        else:
            messagebox.showerror('ERROR','Please enter the customer name.')
import pywhatkit
#from import_mobile_no import MobileNo
from urllib.parse import quote            
def send_msg():
    if flower1_quantity!=0 or flower2_quantity!=0 or flower3_quantity!=0:
        if qty1 != 0 and qty2 == 0 and qty3 == 0:
            Msg = 'Thankyou for choosing _Pushpamayam_ Mr./Mrs. '+ customer_entry.get() +'.  Your total bill is Rs. '+str(total_price)+'. You ordered '+str(qty1)+' Anemones. Thank you! We will love to see you again!'
        elif qty1 == 0 and qty2 != 0 and qty3 == 0:
            Msg = 'Thankyou for choosing _Pushpamayam_  Mr./Mrs. '+ customer_entry.get() +'.  Your total bill is Rs. '+str(total_price)+'. You ordered '+str(qty2)+' White Roses. Thank you! We will love to see you again!'
        elif qty1 == 0 and qty2 == 0 and qty3 != 0:
            Msg = 'Thankyou for choosing _Pushpamayam_ Mr./Mrs. '+ customer_entry.get() +'.  Your total bill is Rs. '+str(total_price)+'. You ordered '+str(qty3)+' Tulips. Thank you! We will love to see you again!'
        elif qty1 != 0 and qty2 != 0 and qty3 == 0:
            Msg = 'Thankyou for choosing _Pushpamayam_ Mr./Mrs. '+ customer_entry.get() +'.  Your total bill is Rs. '+str(total_price)+'. You ordered '+str(qty1)+' Anemones and '+str(qty2)+' White Roses. Thank you! We will love to see you again!'
        elif qty1 == 0 and qty2 != 0 and qty3 != 0:
            Msg = 'Thankyou for choosing _Pushpamayam_ Mr./Mrs. '+ customer_entry.get() +'.  Your total bill is Rs. '+str(total_price)+'. You ordered '+str(qty2)+' White Roses and '+str(qty3)+' Tulips. Thank you! We will love to see you again!'
        elif qty1 != 0 and qty2 == 0 and qty3 != 0:
            Msg = 'Thankyou for choosing _Pushpamayam_ Mr./Mrs. '+ customer_entry.get() +'.  Your total bill is Rs. '+str(total_price)+'. You ordered '+str(qty1)+' Anemones and '+str(qty3)+' Tulips. Thank you! We will love to see you again!'
        elif qty1 != 0 and qty2 != 0 and qty3 != 0: 
            Msg = 'Thankyou for choosing our _Pushpamayam_  Mr./Mrs. '+ customer_entry.get() +'.  Your total bill is Rs. '+str(total_price)+'. You ordered '+str(qty1)+' Anemones, '+str(qty2)+' White Roses and '+str(qty3)+' Tulips. Thank you! We will love to see you again!'
        now = datetime.now()
        hr = int(now.strftime("%H"))
        min = int(now.strftime("%M")) + 2
        MobileNo = "+91 "+number_entry.get()
        pywhatkit.sendwhatmsg(MobileNo,Msg,hr,min)
    
    
    
                

variable1 = StringVar()
variable2 = StringVar()
variable3 = StringVar()




frame1 = customtkinter.CTkFrame(app,bg_color='#000',fg_color='#000',width=724,height=195)
frame1.place(x=0,y=0)

frame2 = customtkinter.CTkFrame(app,bg_color='#000',fg_color='#0E0F0F',width=724,height=440)
frame2.place(x=0,y=195)


image1 = Image.open("/home/hp/Desktop/vscode/CustTk_flower_project/top_banner_flower.png").resize((724,195))#!!!two bracks not one
photo1 = ImageTk.PhotoImage(image1)

image1_label = Label(frame1,image=photo1,bg='#000')
image1_label.place(x=0,y=0)
#image1_label.pack()

p1_frame = customtkinter.CTkFrame(frame2,bg_color='#0E0F0F',fg_color='#333333',corner_radius=0,width=228,height=320)
p1_frame.place(x=10,y=20)
image2 = Image.open("/home/hp/Desktop/vscode/CustTk_flower_project/violet.jpg").resize((228,270))
photo2 = ImageTk.PhotoImage(image2)
image2_label = Label(p1_frame,image=photo2,bg='#333333')
image2_label.place(x=0,y=0)
#image2_label.pack()
p1_name_label = customtkinter.CTkLabel(p1_frame,font=font1,text='',text_color='#fff',bg_color='#333333')
p1_name_label.place(x=17,y=200)
p1_quatity = customtkinter.CTkComboBox(p1_frame,font=font1,text_color='#000',fg_color='#fff',dropdown_hover_color='#06911f',button_color='#f67a0d',button_hover_color='#f67a0d',variable=variable1,width=120)
p1_quatity.set('0')
p1_quatity.place(x=40,y=270)

p2_frame = customtkinter.CTkFrame(frame2,bg_color='#0E0F0F',fg_color='#333333',corner_radius=0,width=228,height=320)
p2_frame.place(x=248,y=20)
image3 = Image.open("/home/hp/Desktop/vscode/CustTk_flower_project/white roses.jpg").resize((228,270))
photo3 = ImageTk.PhotoImage(image3)
image3_label = Label(p2_frame,image=photo3,bg='#333333')
image3_label.place(x=0,y=0)
#image3_label.pack()
p2_name_label = customtkinter.CTkLabel(p2_frame,font=font1,text='',text_color='#fff',bg_color='#333333')
p2_name_label.place(x=40,y=200)
p2_quatity = customtkinter.CTkComboBox(p2_frame,font=font1,text_color='#000',fg_color='#fff',dropdown_hover_color='#06911f',button_color='#f67a0d',button_hover_color='#f67a0d',variable=variable2,width=120)
p2_quatity.set('0')
p2_quatity.place(x=40,y=270)

p3_frame = customtkinter.CTkFrame(frame2,bg_color='#0E0F0F',fg_color='#333333',corner_radius=0,width=228,height=320)
p3_frame.place(x=486,y=20)
image4 = Image.open("/home/hp/Desktop/vscode/CustTk_flower_project/red tulip.jpg").resize((228,270))
photo4 = ImageTk.PhotoImage(image4)
image4_label = Label(p3_frame,image=photo4,bg='#333333')
image4_label.place(x=0,y=0)
#image4_label.pack()
p3_name_label = customtkinter.CTkLabel(p3_frame,font=font1,text='',text_color='#fff',bg_color='#333333')
p3_name_label.place(x=23,y=200)
p3_quatity = customtkinter.CTkComboBox(p3_frame,font=font1,text_color='#000',fg_color='#fff',dropdown_hover_color='#06911f',button_color='#f67a0d',button_hover_color='#f67a0d',variable=variable3,width=120)
p3_quatity.set('0')
p3_quatity.place(x=40,y=270)
#-----------------------------------------------------------------------------------------------------------

customer_label = customtkinter.CTkLabel(frame2,font=font1,text='Customer: ',text_color='#fff',bg_color='#0E0F0F')
customer_label.place(x=40,y=370)

customer_entry = customtkinter.CTkEntry(frame2,font=font1,text_color='#000',fg_color='#fff',border_color='#fff',width=150)
customer_entry.place(x=150,y=370)

checkout_button = customtkinter.CTkButton(frame2,command=checkout,font=font1,text_color='#fff',text='ORDER',fg_color='#410ae3',hover_color='#3303c0',bg_color='#0e0f0f',cursor = 'hand2',corner_radius=30,width=160,height=50)
checkout_button.place(x=340,y=360)

price_label = customtkinter.CTkLabel(frame2,font=font1,text='',text_color='#0f0',bg_color='#0E0F0F')
price_label.place(x=540,y=370)

wp_image = Image.open("/home/hp/Desktop/vscode/CustTk_flower_project/wp_img.png").resize((30,30))
wp_img = ImageTk.PhotoImage(wp_image)

send_button = customtkinter.CTkButton(frame2,image= wp_img,text= " ",command=send_msg,font=font1,fg_color='#0E0F0F',hover_color='#0E0F0F',bg_color='#0E0F0F',cursor = 'hand2',corner_radius=30,width= 30,height= 30)
send_button.place(x=498,y=405)

number_entry = customtkinter.CTkEntry(frame2,font=font1,text_color='#000',fg_color='#fff',border_color='#fff',width=150, height= 29)
number_entry.place(x=568,y=406)

get_flowers()
get_quantity()

app.mainloop()

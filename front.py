import tkinter as tk
import ghe

def ent_email_btn1_click(event):
    if sub.get() == 'Email':
        sub.config(state=tk.NORMAL)
        sub.delete(0, tk.END)
    else:
        sub.config(state=tk.NORMAL)

def ent_ghurl_btn1_click(event):
    if url_entry_output.get() == 'Sample URL':
        ent_ghurl.config(state=tk.NORMAL)
        ent_ghurl.delete(0, tk.END)
    else:
        ent_ghurl.config(state=tk.NORMAL)

def ent_email_btn1_unclick(event):
    if sub.get() == '':
        sub.config(state=tk.NORMAL)
        sub.insert(0, 'Email')
        sub.config(state=tk.DISABLED)
    elif sub.get() == 'Email':
        sub.delete(0, tk.END)
        sub.config(state=tk.DISABLED)
    else:
        sub.config(state=tk.DISABLED)

def ent_ghurl_btn1_unclick(event):
    if ent_ghurl.get() == '':
        ent_ghurl.config(state=tk.NORMAL)
        ent_ghurl.insert(0, 'Sample URL')
        ent_ghurl.config(state=tk.DISABLED)
    elif ent_ghurl.get() == 'Sample URL':
        pass
        # ent_ghurl.delete(0, tk.END)
        # ent_ghurl.insert(0, 'Sample URL')
        ent_ghurl.config(state=tk.DISABLED)
    else:
        ent_ghurl.config(state=tk.DISABLED)


def display_output(output):
    text.configure(state='normal')
    text.delete('1.0', tk.END)
    text.insert(tk.END, output)
    text.configure(state='disabled')


def get_languages_used():
    ghurl = ent_ghurl.get()
    if not ghurl.startswith('https://github.com/'):
        # clear the outut area
        display_output("")
        return
    languages_used_list = ghe.get_languages_used(ghurl)
    languages_used_str = "\n".join(languages_used_list)
    display_output(languages_used_str)
    with open("lang_data.txt",'w')as f:
     f.write(languages_used_str)

 

def is_valid_ghurl(ghurl):
    if not ghurl.startswith('https://github.com/'):
        return False
    return True

def get_repo_stats():
    ghurl = ent_ghurl.get()
    if not is_valid_ghurl(ghurl):
        display_output("")
        return
    s = ghe.get_repo_stats(ghurl)
    display_output(s)
    with open("repo_data.txt",'w')as f:
     f.write(s)



def get_open_issues():
    ghurl = ent_ghurl.get()
    if not ghurl.startswith('https://github.com/'):
        display_output("ERROR: Invalid URL")
        return
    open_issues_list = ghe.get_open_issues(ghurl)
    open_issues_str ='\n'.join(open_issues_list)
    display_output(open_issues_str)
    with open("issue_data.txt",'w')as f:
     f.write(open_issues_str)

def get_open_prs():
    ghurl=ent_ghurl.get()
    if not is_valid_ghurl(ghurl):
        display_output("ERROR:Invalid URL")
        return
    pr_issues_list=ghe.get_open_pulls(ghurl) 
    pr_issues_str='\n'.join(pr_issues_list)
    display_output(pr_issues_str)
    with open("pr_data.txt",'w')as f:
     f.write(pr_issues_str)

def valid_email(email):
    if email == '' or email == 'Email' or '@' not in email:
        return False
    return True

def check():
   f=open("emails.txt",'r').readlines()
   seen = set(f)
   for line in f:
          line_lower = line.lower()
          if line_lower in seen:
               return True
          return  False
    


def subscribe_email():
    # Get the email address and store to a file
    email = sub.get()
    print(email)
    if not valid_email(email):
        display_output("Invalid Email")
        return
    print(email)   
    ghe.save_email(email)
     

def mail_info():
    ghe.send_mail(body="""This is a skillaura internship program. 
    The following mail consists information of a github repository.
    Please refer to the below PDFs for more details""")

    
    


def subscribers():
    ghurl=ent_ghurl.get()
    if not is_valid_ghurl(ghurl):
        display_output("ERROR:Invalid URL")
        return
    subscriber_list=ghe.get_subscriber(ghurl)
    subscribers_str='\n'.join(subscriber_list)
    display_output(subscribers_str)
    




main_window = tk.Tk()

main_window.title("GitHub Repo Explorer")
main_window.resizable(0, 0)

# Frame for main Label
frm_ghurl = tk.LabelFrame(main_window,bg="cornflower blue",fg="black")  # , padx=15, pady=15)
frm_ghurl.pack()  # fill="both", expand="yes")

lbl_title = tk.Label(frm_ghurl, text="GitHub Repo Explorer",bg="cornflower blue",fg="maroon", font='Charter 32 bold', width=50)
lbl_title.pack(side="top", fill="both", expand="yes")


lbl_ghurl = tk.Label(frm_ghurl, text='GitHub Repo URL',bg="cornflower blue",fg="black", font='Helvetica 16 bold', width=15)
lbl_ghurl.pack(side=tk.LEFT)


# URL Entry
url_entry_output = tk.StringVar()
ent_ghurl = tk.Entry(frm_ghurl, textvariable=url_entry_output,bg="light grey",fg="black", font='times 13', width=72)
ent_ghurl.insert(0, 'URL')
ent_ghurl.config(state=tk.DISABLED)
ent_ghurl.bind("<Button-1>", ent_ghurl_btn1_click)
ent_ghurl.bind('<Leave>', ent_ghurl_btn1_unclick)
ent_ghurl.pack(side=tk.LEFT, padx=45, pady=5)

# frame for button

button=tk.LabelFrame(main_window,bg="cornflower blue",padx=15,pady=15)
button.pack(side=tk.TOP,anchor=tk.W,fill="both",expand="yes")

# buttons label


lang=tk.Button(button,text="languages used",font="times 15",width=16,fg="black",bg="rosy brown",command=get_languages_used)
lang.grid(row=0,column=0)


repo=tk.Button(button,text="Repo Stats",font="times 15",width=16,fg="black",bg="rosy brown",command=get_repo_stats)
repo.grid(row=1,column=0)


oi=tk.Button(button,text="open Issues",font="times 15",width=16,fg="black",bg="rosy brown",command=get_open_issues)
oi.grid(row=2,column=0)


op=tk.Button(button,text="Pull Requests",font="times 15",width=16,fg="black",bg="rosy brown",command=get_open_prs)
op.grid(row=3,column=0)


subscriber=tk.Button(button,text="Subscribers",font="times 15",width=16,fg="black",bg="rosy brown",command=subscribers)
subscriber.grid(row=4,column=0)


lang.bind('<Motion>', lambda _: lang.config(bg='gray', highlightbackground='blue', fg='black'))
lang.bind('<Leave>', lambda _: lang.config(bg='white', highlightbackground='white', fg='black'))


repo.bind('<Motion>', lambda _: repo.config(bg='gray', highlightbackground='blue', fg='black'))
repo.bind('<Leave>', lambda _: repo.config(bg='white', highlightbackground='white', fg='black'))

oi.bind('<Motion>', lambda _: oi.config(bg='gray', highlightbackground='blue', fg='black'))
oi.bind('<Leave>', lambda _: oi.config(bg='white', highlightbackground='white', fg='black'))

op.bind('<Motion>', lambda _: op.config(bg='gray', highlightbackground='blue', fg='black'))
op.bind('<Leave>', lambda _: op.config(bg='white', highlightbackground='white', fg='black'))

subscriber.bind('<Motion>', lambda _: subscriber.config(bg='gray', highlightbackground='blue', fg='black'))
subscriber.bind('<Leave>', lambda _: subscriber.config(bg='white', highlightbackground='white', fg='black'))

# frame for output box

output=tk.LabelFrame(button,padx=2,pady=2,width=150)
output.grid(row=0,column=2,rowspan=5,padx=9,pady=9)

# text box for buttons

text=tk.Text(output,bg="light grey",fg="black")
text.pack(side=tk.RIGHT,anchor=tk.E,expand=tk.YES)
text.configure(state='disabled')

#frame for email entry

email_f=tk.LabelFrame(main_window,bg="cornflower blue",padx=9,pady=9)
email_f.pack(fill="both",expand="yes")

# entry for email

sub=tk.StringVar()
sub=tk.Entry(email_f,textvariable=sub,bg="light grey",fg="black",font="times 13",width=70)
sub.insert(0,'E-mail ID')
sub.config(state=tk.DISABLED)
sub.bind("<Button-1>", ent_email_btn1_click)
sub.bind('<Leave>', ent_email_btn1_unclick)
sub.pack(side=tk.LEFT,  padx=10)

# button for subscription

email1=tk.Button(email_f,text="Subscribe",font="times 15",width=16,fg="black",bg="rosy brown",command=subscribe_email)
email1.pack(side=tk.LEFT,padx=15)
email1.bind('<Motion>', lambda _: email1.config(bg='gray', highlightbackground='blue', fg='black'))
email1.bind('<Leave>', lambda _: email1.config(bg='white', highlightbackground='white', fg='black'))

# button for send mail
send=tk.Button(email_f,text="send mail",font="times 15",width=16,fg="black",bg="rosy brown",command=mail_info)
send.pack(side=tk.LEFT,padx=15)
send.bind('<Motion>', lambda _: send.config(bg='gray', highlightbackground='black',fg='black')) #while clicking on button
send.bind('<Leave>', lambda _: send.config(bg='white', highlightbackground='blue',fg='black')) #after clicking on button


main_window.mainloop()








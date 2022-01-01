from django.shortcuts import render, redirect
from .models import *
from datetime import datetime as dt
from datetime import timedelta, time
import calendar
import io
import bcrypt
import urllib, base64
from django.db import connection
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def index(request):
    return render(request, "title_page.html")


def login(request):
    message = ""
    user_id = []
    if request.method=="POST":
        cursor = connection.cursor()
        username = request.POST.get("username",'')
        password = request.POST.get("password",'')
        cursor.execute("select UID, username, password from budget_app_credentials where username=%s;",[username])
        
        try:
            user_id = list(cursor.fetchone())
            print(user_id[0])
        except TypeError:
            pass
        if not user_id:
                message = "No user with above credentials"
        elif user_id and bcrypt.checkpw(password.encode('utf-8'), user_id[2]):
            return redirect(f"/budget/{user_id[0]}/overview/")
        else:
            if password!=user_id[2]:
                message = "incorrect password"
            
        cursor.close()
        connection.close()
    return render(request, "login.html", {'message':message})


def register(request):
    context = ""
    user_id = []
    if request.method=="POST":
        cursor = connection.cursor()
        username = request.POST.get("Username",'')
        password = request.POST.get("Password",'')
        fullname = request.POST.get("FullName",'')
        email = request.POST.get("email",'')
        phone = request.POST.get("phone",'')
        cursor.execute("select UID from budget_app_credentials where username=%s",[username])
        try:
            user_id = list(cursor.fetchone())
            context = "This username is already taken"
        except TypeError:
            password = bytes(password,encoding="utf-8")
            encrypted_password = bcrypt.hashpw(password, bcrypt.gensalt(10))

            cursor.execute("insert into budget_app_credentials(fullname,username,email_id, phone_no,password) values(%s,%s,%s,%s,%s)",[fullname, username,email, phone, encrypted_password])

            pk = cursor.execute("select UID from budget_app_credentials where username=%s;",[username])

            llist = ['travel', 'gift', 'booking', 'vehicle']
            for i in llist:
                cursor.execute("insert into budget_app_expense_categories(user, cat_type) values(%s, %s)", [pk, i])


            return redirect("/login/")
        finally:
            cursor.close()
            connection.close()

    return render(request, "register.html", {'context':context})


def overview_page(request, pk):
    month_budget = 0
    all_expenses = []
    graphic = ""
    expense_types = []
    bar_plot = ""
    cursor = connection.cursor()
    try:
        cur_month = dt.now().month
        cur_year = dt.now().year
        cursor.execute("select total_budget, left_budget from budget_app_budget where user_exp=%s and month=%s and year=%s", [pk,cur_month, cur_year])
        month_budget = list(cursor.fetchone())
        month_budget.append(month_budget[0]-month_budget[1])

        cursor.execute("select expense_type, expense_amnt,expense_time from budget_app_expense where user=%s and expense_date=%s", [pk, dt.now().strftime("%Y-%m-%d")])
        all_expenses = list(cursor.fetchall())

        cursor.execute("select cat_type from budget_app_expense_categories where user=%s", [pk])
        expense_types = list(cursor.fetchall())
    
        plt.clf()
        categories = []
        amounts = []
        

        cursor.execute('select expense_type, sum(expense_amnt) from budget_app_expense  where user=%s and expense_date like "%%-'+'%s'+'-%%" group by expense_type', [pk, dt.now().month])
        try: 
            expense_amnts = list(cursor.fetchall())
            for i in expense_amnts:
                categories.append(i[0])
                amounts.append(int(i[1]))
            plt.bar(categories, amounts, color=(0.2,0.15,0.77,0.7), width=0.2)
        except:   
            print("except")
            if not categories:
                categories = []
                for i in expense_types:
                    categories.append(i[0])
                plt.bar(categories, [0], color=(0.2,0.15,0.77,0.7))
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches = 'tight', transparent = True)
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        bar_plot = base64.b64encode(image_png)
        bar_plot = bar_plot.decode('utf-8')


        
        plt.clf()
        


        plt.rcParams.update({'font.size' : 15})
        labels = ['Balance', 'Spent']

        values = [month_budget[1], month_budget[0]-month_budget[1]]
        plt.pie(x=values, labels=labels, colors=[(0.2,0.15,0.77,0.7), (0.4,0.8,0.99,1)], radius=0.65)


        circle = plt.Circle(xy=(0,0), radius=0.55, facecolor='white')
        circle.set_alpha(0.6)
        plt.gca().add_artist(circle)

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches = 'tight', transparent = True)
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')

        

    except TypeError:
        pass

    if request.method=="POST":
        if "add-new-expense" in request.POST:
            exp_type = request.POST.get('type','')
            exp_amt = request.POST.get('amt','')
            exp_date = request.POST.get('date','')
            exp_date = dt.strptime(exp_date, '%Y-%m-%d')
            now = str(dt.now())[11:19].split(':')
            exp_time =  time(int(now[0]), int(now[1]), int(now[2]))       
            exp_day = calendar.day_name[dt.date(exp_date).weekday()]
            cursor.execute('insert into budget_app_expense(user, expense_type, expense_amnt, expense_day, expense_date, expense_time) values(%s,%s,%s,%s,%s,%s)', [pk, exp_type, exp_amt, exp_day, str(exp_date)[0:10], exp_time])
            cursor.execute('update budget_app_budget set left_budget=%s where user_exp=%s and month=%s and year=%s ', [int(month_budget[1])-int(exp_amt), pk, int(dt.now().month), int(dt.now().year)])
            return redirect(f'/budget/{pk}/overview/')

        else:
            for i in all_expenses:
                if i[2] in request.POST:
                    cursor.execute('select expense_amnt from  budget_app_expense where user=%s and expense_time=%s', [pk, i[2]])
                    amnt = cursor.fetchone()[0]
                    cursor.execute('delete from budget_app_expense where user=%s and expense_time=%s', [pk, i[2]])
                    cursor.execute('update budget_app_budget set left_budget=%s where user_exp=%s and month=%s and year=%s ', [int(month_budget[1])+int(amnt), pk, int(dt.now().month), int(dt.now().year)])
                    return redirect(f"/budget/{pk}/overview/")
        cursor.close()
        connection.close()
    return render(request, 'budget_app/overview.html', {'pk':pk, 'month_budget':month_budget, 'all_expenses':all_expenses, 'graphic':graphic, 'expense_types': expense_types, 'bar_plot':bar_plot})


def home_page(request, pk):
    cursor = connection.cursor()
    monthly_expense_stats = []
    monthly_epxense_plots = []
    monthly_budget_stats = []
    monthly_budget_charts = []    

    for i in range(1,dt.now().month+1):
        temp = []
        cursor.execute('select expense_type, sum(expense_amnt) from budget_app_expense  where user=%s and expense_date like "%s-'+'%s'+'-%%" group by expense_type',[pk,  dt.now().year, i])
        temp = list(cursor.fetchall())
        monthly_expense_stats.append(temp)

    
        temp = []
        cursor.execute("select total_budget, left_budget from budget_app_budget where user_exp=%s and month=%s and year=%s", [pk, i, dt.now().year])
        try:
            temp = list(cursor.fetchone())
            temp.append(temp[0]-temp[1])
        except TypeError:
            temp = [0,0,0]
        monthly_budget_stats.append(temp)
    ctr = 0
    for indivisual in monthly_budget_stats:
        ctr +=1
        plt.clf()
        plt.rcParams.update({'font.size' : 25})
        labels = ['Balance', 'Spent']

        if indivisual[0] == 0:
            values = [100,0]
        else:
            values = [indivisual[1], indivisual[2]]
        
        plt.pie(x=values, labels=labels, colors=[(0.2,0.15,0.77,0.7), (0.4,0.8,0.99,1)])
        
        plt.title(calendar.month_name[ctr])
        
        circle = plt.Circle(xy=(0,0), radius=0.75, facecolor='white')
        circle.set_alpha(0.6)
        plt.gca().add_artist(circle)

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches = 'tight', transparent = True)
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')

        monthly_budget_charts.append(graphic)

    ctr = 0
    for month_expense in monthly_expense_stats:
        ctr+=1
        categories = []
        amounts = []
        temp = []

        plt.clf()
        plt.rcParams.update({'font.size' : 20})
        for j in month_expense:
            categories.append(j[0])
            amounts.append(int(j[1]))
        if categories:
            plt.bar(categories, amounts, color=(0.2,0.15,0.77,0.7), width=0.2)
          
        elif  not categories:
            cursor.execute("select cat_type from budget_app_expense_categories where user=%s", [pk])
            expense_types = list(cursor.fetchall())
            for j in expense_types:
                categories.append(j[0])
            plt.bar(categories, [0], color=(0.2,0.15,0.77,0.7))

        plt.xlabel("Categories")
        plt.ylabel("Amount")
        plt.title(calendar.month_name[ctr])
    
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches = 'tight', transparent = True)
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        bar_plot = base64.b64encode(image_png)
        bar_plot = bar_plot.decode('utf-8')

        monthly_epxense_plots.append(bar_plot)

    monthly_details = zip(monthly_budget_stats, monthly_budget_charts)
            

    if request.method=="POST":
        if 'add-category' in request.POST:
            new_category = request.POST.get("cat-input","")
            cursor.execute("insert into budget_app_expense_categories(user, cat_type) values(%s,%s)", [pk, new_category])
            return redirect(f"/budget/{pk}/home")
        else:
            for i in expense_types:
                if i[0] in request.POST:
                    cursor.execute("delete from budget_app_expense_categories where user=%s and cat_type=%s",[pk,i[0]])
                    return redirect(f"/budget/{pk}/home")

    return render(request, 'budget_app/home.html', {'pk':pk, 'monthly_plots':monthly_epxense_plots, 'monthly_details':monthly_details, 'expense_categories':expense_types})


def profile_page(request, pk):
    cursor = connection.cursor()
    budget = 0
    cursor.execute('select * from budget_app_credentials where UID=%s',[pk])
    user_profile = cursor.fetchone()
    month = dt.now().month
    year = dt.now().year
    cursor.execute('select total_budget from budget_app_budget where user_exp=%s and month=%s and year=%s',[pk, month, year])
    budget = cursor.fetchone()
    month_name = calendar.month_name[dt.now().month]

    if request.method=='POST':
        if 'apply'  in  request.POST:
            print("execite")
            new_budget = int(request.POST.get("budget"))
            username = request.POST.get("username",'')
            fullname = request.POST.get("name",'')
            email = request.POST.get("email-id",'')
            phone = request.POST.get("phone-no",'')

            print("execute")
            cursor = connection.cursor()
            cursor.execute('update budget_app_credentials set fullname=%s ,username=%s ,email_id=%s , phone_no=%s where UID=%s ', [fullname, username, email, phone, pk])


            try:
                cursor.execute('select total_budget, left_budget from budget_app_budget where user_exp=%s and month=%s and year=%s',[pk, month, year])
                old_budget = cursor.fetchone()
                expenses_made = old_budget[0]-old_budget[1]
                cursor.execute('update budget_app_budget set total_budget=%s, left_budget=%s where user_exp=%s and month=%s and year=%s', [new_budget, new_budget-expenses_made, pk, month, year])
                
                
            except:
                cursor.execute('insert into budget_app_budget(user_exp, month, year, total_budget, left_budget) values(%s, %s, %s, %s, %s)', [pk,month,year,new_budget, new_budget])
            finally:
                cursor.close() 
                connection.close()
                
            return redirect(f'/budget/{pk}/profile')

    return render(request, 'budget_app/profile.html', {'pk':pk, 'month_name':month_name, 'user_profile':user_profile, 'budget':budget})
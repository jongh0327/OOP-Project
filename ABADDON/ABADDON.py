from Tkinter import*
import random
import tkMessageBox
import time

window=Tk()
window.title("ABADDON")

main=Frame(window)
village=Frame(window)
shop=Frame(window)
bank=Frame(window)
stat=Frame(window)
dungeon_L=Frame(window)
dungeon=Frame(window)
death=Frame(window)

############################### 변수
Data=[1,25,9,0,100,0,0,0,0]

deposit_n=IntVar()
withdraw_n=IntVar()

monster_list=[[],[],[],[]]
boss_list=[]

f=open("./monster1.txt",'r')
for i in range(3):
    for j in range(5):
        k=f.readline().split()
        monster_list[i].append(k)

f=open("./boss.txt",'r')
for i in range(3):
    k=f.readline().split()
    monster_list[3].append(k)

dungeon_number=0
dungeon_counter=1
boss_count=0

################################   
class Player(object):
    def __init__(self,Level=1,Atk=9,Hp=25,Weapon=0,Armor=0,money=100,account=0,potion=0,exp=0):
        self.Lv=Level
        self.Atk=Atk
        self.Hp=Hp
        self.Weapon=Weapon
        self.Armor=Armor
        self.money=money
        self.account=account
        self.potion=potion    
        self.exp=exp
    
    def deposit(self,a):
        global my_money,in_account
        if a<0:
            pass
        elif a<=self.money:
            self.money-=a
            self.account+=a
            my_money.config(text="Money "+str(self.money))
            in_account.config(text="Account "+str(self.account))
        
    def withdraw(self,a):
        global my_money,in_account
        if a<0:
            pass
        elif a<=self.account:
            self.money+=a
            self.account-=a
            my_money.config(text="Money "+str(self.money))
            in_account.config(text="Account "+str(self.account))            

    def update_money(self):
        global my_money
        my_money.config(text="Money "+str(player.money))

    def buy_potion(self):
        if self.money>=100:
            self.money-=100
            self.potion+=1
        self.update_stat()
        
    def upgrade_weapon(self):
        if self.money>=self.Lv*30+20:
            self.money-=self.Lv*30+20          
            self.Lv+=1
            self.Weapon+=2
            self.Atk+=2
            self.update_stat()
                
    def upgrade_armor(self):
        if self.money>=self.Lv*30+20:
            self.money-=self.Lv*30+20
            self.Lv+=1
            self.Armor+=5
            self.Hp+=5
            self.update_stat()
        
    def die(self):
        self.Lv=1
        self.Atk=9
        self.Hp=25
        self.Weapon=0
        self.Armor=0
        self.money=0
        self.potion=0
        self.exp=0
        
    def Attack(self,monster):        
        global MyHp
        global maxHp
        global dungeon_counter
        global boss_count
                
        if self.Atk>=monster.Hp:
            monster.Hp=0
            Hp.config(text="HP "+str(monster.Hp)+"/"+maxHp)
            name.config(text="Money +"+str(monster.money))
            self.money+=int(monster.money)
            
            Atk_b.grid_forget()
            Potion_b.grid_forget()
            Potion_b.grid(row=6,columnspan=2)
            if monster.name=='lethe':
                if boss_count==0:
                    boss_count=1
                Potion_b.grid_forget()
                Return_b.grid(row=6,columnspan=2)
            elif monster.name=="hades":
                if boss_count==1:
                    boss_count=2
                Potion_b.grid_forget()
                Return_b.grid(row=6,columnspan=2)           
            elif monster.name=="abaddon":
                boss_count+=1
                if  boss_count==3:
                    tkMessageBox._show("Congratulations!!!","You Have Finished The Game!!!! \n Thanks For Enjoying It!!! \n \n Made By Lee Jonghyun")                
                Potion_b.grid_forget()
                Return_b.grid(row=6,columnspan=2)
            elif dungeon_counter==11:
                Retreat_b.grid(row=7,column=0)
                Boss_b.grid(row=7,column=1)
            else:                
                Retreat_b.grid(row=7,column=0)
                Onward_b.grid(row=7,column=1)
        else:
            monster.Hp-=self.Atk
            Hp.config(text="HP "+str(monster.Hp)+"/"+maxHp)
        if monster.Hp!=0:
            monster.Attack(self)
            
    def Potion(self,monster):
        global MyHp       
        if self.potion>=1:
            self.potion-=1
            Potion_b.config(text="Potion("+str(player.potion)+")",font=("Courier",15))
            if MyHp>=self.Hp/2:
                MyHp=self.Hp 
                My_Hp.config(text="HP "+str(MyHp))
            else:
                MyHp+=self.Hp/2
                My_Hp.config(text="HP "+str(MyHp))
            if monster.Hp!=0:
                monster.Attack(self)            
                
    def Retreat(self):
        Return_b.grid_forget()
        Retreat_b.grid_forget()
        Onward_b.grid_forget()
        Boss_b.grid_forget()
        Atk_b.grid(row=5,column=0)
        Potion_b.grid(row=5,column=1)
        transfer(dungeon,village)
        
    def update_stat(self):
        my_money.config(text="Money "+str(self.money))
        in_account.config(text="Account "+str(self.account))
        level_show.config(text="Level "+str(player.Lv))
        hp_show.config(text="Hp "+str(player.Hp))
        atk_show.config(text="Atk "+str(player.Atk))
        money_show.config(text="Money "+str(player.money))
        potion_show.config(text="Potion "+str(player.potion))
        potion_buy_b.config(text="Potion("+str(player.potion)+") 100G")
        shop_money.config(text="Money "+str(player.money))
        weapon_b.config(text="Upgrade Weapon "+str(player.Lv*30+20)+"G")
        armor_b.config(text="Upgrade Armor "+str(player.Lv*30+20)+"G")
        My_Atk.config(text="Atk "+str(player.Atk))
            
class Monster(object):    
    def __init__(self,a,n):
        self.name=monster_list[a][n][0]
        self.Hp=int(monster_list[a][n][1])
        self.Atk=int(monster_list[a][n][2])
        self.image=monster_list[a][n][3]
        self.money=monster_list[a][n][4]
        
    def Attack(self,player):
        global MyHp
        
        if MyHp<=monster.Atk:
            MyHp=0
            My_Hp.config(text="HP "+str(MyHp))
            player.die()
            save()
            transfer(dungeon,death)
        else:
            MyHp-=monster.Atk
            My_Hp.config(text="HP "+str(MyHp))
    
###############################
def transfer(a,b):                #장소이동 함수
    a.pack_forget()
    b.pack()
    player.update_stat()

    if boss_count==1:
        blank2.grid(row=4,columnspan=2)
        dungeon2_b.grid(row=3,columnspan=2)
    elif boss_count>=2:
        blank2.grid(row=4,columnspan=2)
        blank3.grid(row=6,columnspan=2)
        dungeon3_b.grid(row=5,columnspan=2)
        dungeon2_b.grid(row=3,columnspan=2)    
    
def to_dungeon(a):              #던전이동함수
    dungeon_L.pack_forget()
    dungeon.pack()
    global dungeon_number
    global dungeon_counter
    
    dungeon_number=a-1
    dungeon_counter=1
    Explore()

def save():
    global player
    f=open("./save_file.txt",'w')
    Data=[player.Lv,player.Atk,player.Hp,player.Weapon,player.Armor,player.money,player.account,player.potion,boss_count]
    for i in range(len(Data)):
        f.write(str(Data[i])+" ")

def load():
    global boss_count
    
    f=open("./save_file.txt",'r')
    Data=f.read().split()
    for i in range(len(Data)):
        Data[i]=int(Data[i])
        
    player.Lv=Data[0]
    player.Atk=Data[1]
    player.Hp=Data[2]
    player.Weapon=Data[3]
    player.Armor=Data[4]
    player.money=Data[5]
    player.account=Data[6]
    player.potion=Data[7]
    boss_count=int(Data[8])
    
    transfer(main,village)
    player.update_stat()
    
def new_game_c():
    player.Lv=1
    player.Atk=9
    player.Hp=25
    player.Weapon=0
    player.Armor=0
    player.money=100
    player.account=0
    player.potion=0
    transfer(main,village)
    
############################# 
player=Player()
    
###########################   main
title=Label(main,text="ABADDON",font=("Courier",30),fg="red")
title.grid(row=0,columnspan=2)

main_image=PhotoImage(file="./Pictures/pentagram.gif")
image1=Label(main,image=main_image)
image1.grid(row=1,columnspan=2)

new_game=Button(main,text="New",command=new_game_c,font=("Courier",15))
new_game.grid(row=2,columnspan=2)

load_game=Button(main,text="Load",command=load,font=("Courier",15))
load_game.grid(row=3,columnspan=2)

###############################  village
village_image=PhotoImage(file="./Pictures/village.gif")
image2=Label(village,image=village_image)
image2.grid(row=0,columnspan=2)

dungeon_b=Button(village,text="Dungeon",font=("Courier",13),command=lambda: transfer(village,dungeon_L))
dungeon_b.grid(row=1,column=0)

stat_b=Button(village,text="Stat",font=("Courier",13),command=lambda: transfer(village,stat))
stat_b.grid(row=1,column=1)

bank_b=Button(village,text="Bank",font=("Courier",13),command=lambda: transfer(village,bank))
bank_b.grid(row=2,column=0)

shop_b=Button(village,text="Shop",font=("Courier",13),command=lambda: transfer(village,shop))
shop_b.grid(row=2,column=1)

save_b=Button(village,text="Save",font=("Courier",13),command=save)
save_b.grid(row=3,column=0)

back_b=Button(village,text="Back",font=("Courier",13),command=lambda: transfer(village,main))
back_b.grid(row=3,column=1)

#################################   stat
stat_image=PhotoImage(file="./Pictures/stat.gif")
image3=Label(stat,image=stat_image)
image3.grid(row=0,columnspan=2)

level_show=Label(stat,text="Level "+str(player.Lv),font=("Courier",15))
level_show.grid(row=1,columnspan=2)

hp_show=Label(stat,text="Hp "+str(player.Hp),font=("Courier",15))
hp_show.grid(row=2,column=0)

atk_show=Label(stat,text="Atk "+str(player.Atk),font=("Courier",15))
atk_show.grid(row=2,column=1)

money_show=Label(stat,text="Money "+str(player.money),font=("Courier",15))
money_show.grid(row=3,column=0)

potion_show=Label(stat,text="Potion "+str(player.potion),font=("Courier",15))
potion_show.grid(row=3,column=1)

stat_village=Button(stat,text="Back to Village",font=("Courier",13),command=lambda: transfer(stat,village))
stat_village.grid(row=4,columnspan=2)

##################################### bank
bank_image=PhotoImage(file="./Pictures/bank.gif")
image4=Label(bank,image=bank_image)
image4.grid(row=0,columnspan=2)

my_money=Label(bank,text="Money "+str(player.money),font=("Courier",15))
my_money.grid(row=1,columnspan=2)

in_account=Label(bank,text="Account "+str(player.account),font=("Courier",15))
in_account.grid(row=2,columnspan=2)

ask_deposit=Entry(bank,textvariable=deposit_n,font=("Courier",13))
ask_deposit.grid(row=3,column=0)

deposit_b=Button(bank,text="Deposit",font=("Courier",13),command=lambda: player.deposit(deposit_n.get()))
deposit_b.grid(row=3,column=1)

ask_withdraw=Entry(bank,textvariable=withdraw_n,font=("Courier",13))
ask_withdraw.grid(row=4,column=0)

deposit_b=Button(bank,text="Withdraw",font=("Courier",13),command=lambda: player.withdraw(withdraw_n.get()))
deposit_b.grid(row=4,column=1)

bank_village=Button(bank,text="Back to Village",font=("Courier",13), command=lambda: transfer(bank,village))
bank_village.grid(row=5,columnspan=2)

####################################    shop
shop_money=Label(shop,text="Money "+str(player.money),font=("Courier",18))
shop_money.grid(row=1,columnspan=2)

shop_image=PhotoImage(file="./Pictures/shop.gif")
image5=Label(shop,image=shop_image)
image5.grid(row=0,columnspan=2)

potion_buy_b=Button(shop,text="Potion("+str(player.potion)+") 100G",font=("Courier",13), command=player.buy_potion)
potion_buy_b.grid(row=2,columnspan=2)

weapon_b=Button(shop,text="Upgrade Weapon "+str(player.Lv*50)+"G",font=("Courier",13),command=player.upgrade_weapon)
weapon_b.grid(row=3,columnspan=2)

armor_b=Button(shop,text="Upgrade Armor"+str(player.Lv*50)+"G",font=("Courier",13),command=player.upgrade_armor)
armor_b.grid(row=4,columnspan=2)

shop_village=Button(shop,text="Back to Village",font=("Courier",13),command=lambda: transfer(shop,village))
shop_village.grid(row=5,columnspan=2)

####################################   dungeon_L
dungeon_L_image=PhotoImage(file="./Pictures/dungeon_L.gif")
image6=Label(dungeon_L,image=dungeon_L_image)
image6.grid(row=0,columnspan=2)

dungeon1_b=Button(dungeon_L,text="Forgotten Forest",font=("Courier",15),command=lambda: to_dungeon(1))
dungeon1_b.grid(row=1,columnspan=2)

blank1=Label(dungeon_L)
blank1.grid(row=2,columnspan=2)

dungeon2_b=Button(dungeon_L,text="Heretic's Graveyard",font=("Courier",15),command=lambda: to_dungeon(2))

blank2=Label(dungeon_L,text="Recommended Level : 30\n")

dungeon3_b=Button(dungeon_L,text="Grand Archive",font=("Courier",15),command=lambda: to_dungeon(3))

blank3=Label(dungeon_L,text="Recommended Level : 165\n")

dungeon_L_village=Button(dungeon_L,text="Back to Village",font=("Courier",13),command=lambda: transfer(dungeon_L,village))
dungeon_L_village.grid(row=7,columnspan=2)

####################################    death
blank4=Label(death,text="",font=("Courier",40))
blank4.grid(row=0,column=0)

you_die=Label(death,text="You Died",font=("Courier",40,"bold"),fg="red")
you_die.grid(row=1,columnspan=2)

blank5=Label(death,text=" ",font=("Courier",40))
blank5.grid(row=2,column=0)

continue_b=Button(death,text="Continue?",font=("Courier",16),command=lambda: transfer(death,village))
continue_b.grid(row=3,columnspan=2)

######################################################## dungeon
progress=Label(dungeon,text=str(dungeon_counter)+"/10",font=("Courier",18))
progress.grid(row=0,column=0)

name=Label(dungeon,text="| asdfasdf",font=("Courier",18))
name.grid(row=0,column=1)

Hp=Label(dungeon,text="0",font=("Courier",18))
Hp.grid(row=1,columnspan=2)

Atk=Label(dungeon,text="0",font=("Courier",18))
Atk.grid(row=2,columnspan=2)

monster_image=PhotoImage(file="./Pictures/Blank.gif")
image7=Label(dungeon,image=monster_image)
image7.grid(row=3,columnspan=2)

line=Label(dungeon,text="###################################")
line.grid(row=4,columnspan=2)

My_Hp=Label(dungeon,text="Hp "+str(player.Hp),font=("Courier",15))
My_Hp.grid(row=5,column=0)

My_Atk=Label(dungeon,text="Atk "+str(player.Atk),font=("Courier",15))
My_Atk.grid(row=5,column=1)

Atk_b=Button(dungeon,text="Attack",font=("Courier",15),command=lambda: player.Attack(monster))
Atk_b.grid(row=6,column=0)

Potion_b=Button(dungeon,text="Potion("+str(player.potion)+")",font=("Courier",15),command=lambda:player.Potion(monster))
Potion_b.grid(row=6,column=1)

Retreat_b=Button(dungeon,text="Retreat",font=("Courier",15),command=player.Retreat)

Return_b=Button(dungeon,text="Return to Village",font=("Courier",15),command=player.Retreat)

def Boss_battle():
    global dungeon_number
    global monster_image
    global MyHp  
    
    global monster
    global maxHp
    
    Retreat_b.grid_forget()
    Boss_b.grid_forget()
    Atk_b.grid(row=6,column=0)
    Potion_b.grid(row=6,column=1)        
    
    monster=Monster(3,dungeon_number)
    maxHp=str(monster.Hp)
    
    Potion_b.config(text="Potion("+str(player.potion)+")")
    name.config(text=monster.name.upper())
    Hp.config(text="HP "+str(monster.Hp)+"/"+maxHp)
    Atk.config(text="Atk "+str(monster.Atk))
    monster_image=PhotoImage(file="./Pictures/"+monster.image)
    image7.config(image=monster_image)    
    
    
    
def Onward():
    global dungeon_counter
    global dungeon_number
    global monster_image
    global MyHp  
    
    global monster
    global maxHp
    
    Retreat_b.grid_forget()
    Onward_b.grid_forget()
    Atk_b.grid(row=6,column=0)
    Potion_b.grid(row=6,column=1)    
    
    progress.config(text=str(dungeon_counter)+"/10")
    n=random.randint(0,4)
    monster=Monster(dungeon_number,n)
    maxHp=str(monster.Hp)

    Potion_b.config(text="Potion("+str(player.potion)+")")
    name.config(text=monster.name.upper())
    Hp.config(text="HP "+str(monster.Hp)+"/"+maxHp)
    Atk.config(text="Atk "+str(monster.Atk))
    monster_image=PhotoImage(file="./Pictures/"+monster.image)
    image7.config(image=monster_image)

    dungeon_counter+=1    
###########################################################################3
Onward_b=Button(dungeon,text="Continue",font=("Courier",15),command=Onward)
Boss_b=Button(dungeon,text="Boss",font=("Courier",15),command=Boss_battle)
##############################################################################
def Explore():
    global dungeon_counter
    global dungeon_number
    global monster_image
    global MyHp
    
    MyHp=player.Hp    
    
    global monster
    global maxHp
    
    My_Hp.config(text="Hp "+str(player.Hp))
    progress.config(text=str(dungeon_counter)+"/10")
    n=random.randint(0,4)
    monster=Monster(dungeon_number,n)
    maxHp=str(monster.Hp)
    
    My_Hp.grid(row=5,column=0)
    My_Atk.grid(row=5,column=1)
    Atk_b.grid(row=6,column=0)
    Potion_b.grid(row=6,column=1)

    Potion_b.config(text="Potion("+str(player.potion)+")")
    name.config(text=monster.name.upper())
    Hp.config(text="HP "+str(monster.Hp)+"/"+maxHp)
    Atk.config(text="Atk "+str(monster.Atk))
    monster_image=PhotoImage(file="./Pictures/"+monster.image)
    image7.config(image=monster_image)

    dungeon_counter+=1


###############################

def start():
    main.pack()
    mainloop()

    
start()
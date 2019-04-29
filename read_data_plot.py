import sqlite3
import matplotlib.pyplot as plt

conn =sqlite3.connect("data_1.db")
cur = conn.cursor()
cur.execute("SELECT Year, Total, Male, Female, Town, Countryside FROM data")
data_list = cur.fetchall()
conn.commit()
conn.close()

x = []
total = []
male = []
female = []
town = []
countryside = []
for i in range(len(data_list)):
    x.append(data_list[i][0])
    total.append(data_list[i][1])
    male.append(data_list[i][2])
    female.append(data_list[i][3])
    town.append(data_list[i][4])
    countryside.append(data_list[i][5])


plt.figure(figsize=[20,8])
plt.xticks(x,size ='large')
plt.title("Total Population  ")
plt.xlabel("Year")
plt.ylabel("China Total Population / 10 thousands")
plt.yticks(size ='large')
plt.ylim(110000, 150000)
plt.bar(x, total, width =0.5 ,fc='r')
for a, b in zip(x,total):
    plt.text(a, b, '%.0f' % b, ha='center', va= 'bottom',fontsize=11)

plt.savefig('Total.jpg')


plt.figure(figsize=[20,8])
plt.xticks(x,size ='large')
plt.title("Male & Female Population")
plt.xlabel("Year")
plt.ylabel("Male & Female / 10 thousands")
plt.yticks(size ='large')
plt.ylim(60000, 75000)
plt.plot(x, male, marker='o',linestyle='--')
for a, b in zip(x,male):
    plt.text(a, b+100, '%.0f' % b, ha='center', va= 'bottom',fontsize=11)
plt.plot(x, female, marker='*',linestyle=':')
for a, b in zip(x,female):
    plt.text(a, b+100, '%.0f' % b, ha='center', va= 'bottom',fontsize=11)
plt.legend(['Male', 'Female'], loc = "upper right", fontsize=11)
plt.savefig('M&F.jpg')

plt.figure(figsize=[20,8])
plt.xticks(x,size ='large')
plt.title("Town & Countryside Population")
plt.xlabel("Year")
plt.ylabel("Town & Countryside / 10 thousands")
plt.yticks(size ='large')
plt.ylim(30000, 100000)
plt.plot(x, town, marker='x',linestyle='--', c='c')
for a, b in zip(x,town):
    plt.text(a, b-3000, '%.0f' % b, ha='center', va= 'bottom',fontsize=11)
plt.plot(x, countryside, marker='^',linestyle=':', c='k')
for a, b in zip(x,countryside):
    plt.text(a, b+2000, '%.0f' % b, ha='center', va= 'bottom',fontsize=11)
plt.legend(['Town', 'Countryside'], loc = "upper right", fontsize=11)
plt.savefig('T&C.jpg')
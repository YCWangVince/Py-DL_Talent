import sqlite3
import matplotlib.pyplot as plt

conn =sqlite3.connect("data_cpi.db")
cur = conn.cursor()
cur.execute("SELECT Year, CPI, Town_CPI, Countryside_CPI FROM data_cpi")
data_list = cur.fetchall()
conn.commit()
conn.close()

x = []
cpi = []
town_cpi=[]
countryside_cpi = []
total = [1]
for i in reversed(range(len(data_list))):
    x.append(data_list[i][0])
    cpi.append(data_list[i][1]/100-1)
    town_cpi.append(data_list[i][2] / 100 - 1)
    countryside_cpi.append(data_list[i][3] / 100 - 1)
    total.append(total[len(data_list)-i-1]*(cpi[len(data_list)-i-1]+1))

fig = plt.figure(figsize=[20,8])
plt.title("CPI")
plt.xticks(x,size ='large')
ax1 = fig.add_subplot(111)

ax1.set_xlabel("Year")
ax1.set_ylabel("%")
ax1.plot(x, cpi, marker='*',linestyle='--', c='r')
for a, b in zip(x,cpi):
    ax1.text(a, b-0.003, '%.4f' % b, ha='center', va= 'bottom',fontsize=11)
ax1.set_ylim(-0.01,0.07)

ax2 = plt.twinx()
ax2.bar(x, total[1:len(total)], width =0.5 ,fc='g',alpha=0.5)
for a, b in zip(x,total[1:len(total)]):
    ax2.text(a, b+0.01, '%.4f' % b, ha='center', va= 'bottom',fontsize=11)
ax2.set_ylim(0.9,1.3)
fig.legend(['Annual CPI', 'Relative Price to 2008'])
plt.savefig('CPI.jpg')

plt.figure(figsize=[20,8])
plt.title("Town & Countryside CPI")
plt.xticks(x,size ='large')
plt.plot(x, town_cpi, marker = '^', linestyle='--')
for a, b in zip(x[0:3],town_cpi[0:3]):
    plt.text(a, b-0.004, '%.4f' % b, ha='center', va= 'bottom',fontsize=11)
plt.text(x[3], town_cpi[3]+0.002, '%.4f' % town_cpi[3], ha='center', va= 'bottom',fontsize=11)
plt.text(x[4], town_cpi[4]-0.004, '%.4f' % town_cpi[4], ha='center', va= 'bottom',fontsize=11)
for a, b in zip(x[5:10],town_cpi[5:10]):
    plt.text(a, b+0.002, '%.4f' % b, ha='center', va= 'bottom',fontsize=11)

plt.plot(x, countryside_cpi, marker = 'v', linestyle='--')
for a, b in zip(x[0:3],countryside_cpi[0:3]):
    plt.text(a, b+0.002, '%.4f' % b, ha='center', va= 'bottom',fontsize=11)
plt.text(x[3], countryside_cpi[3]-0.004, '%.4f' % countryside_cpi[3], ha='center', va= 'bottom',fontsize=11)
plt.text(x[4], countryside_cpi[4]+0.002, '%.4f' % countryside_cpi[4], ha='center', va= 'bottom',fontsize=11)
for a, b in zip(x[5:10],countryside_cpi[5:10]):
    plt.text(a, b-0.004, '%.4f' % b, ha='center', va= 'bottom',fontsize=11)

plt.ylim(-0.015,0.07)
plt.legend(['Town CPI', 'Countryside CPI'])
plt.savefig('T&C_CPI.jpg')
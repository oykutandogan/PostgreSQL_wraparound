import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- AYARLAR ---
TOTAL_XID = 360  # Gerçekte 4 Milyar, simülasyon için 360 derece
HALF_CYCLE = TOTAL_XID / 2  # 2^31 sınırı (Görünürlük ufku)
FREEZE_AGE = 140 # Bu yaştan sonra satır dondurulmalı (Vacuum Freeze)

# --- DURUM DEĞİŞKENLERİ ---
current_xid = 0
# Veritabanındaki satırlar: {'id': xid, 'frozen': bool}
rows = [] 

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))

def init():
    ax.set_theta_zero_location("N") # 0 noktası yukarıda (Saat 12)
    ax.set_theta_direction(-1) # Saat yönünde dönsün
    ax.set_ylim(0, 1)
    ax.set_yticks([]) # Yarıçap çizgilerini gizle
    ax.set_xticklabels([]) # Derece yazılarını gizle
    return ax,

def update(frame):
    global current_xid, rows
    
    ax.clear()
    init() # Temel ayarları tekrar yükle
    
    # 1. XID İLERLİYOR (Zaman akıyor)
    current_xid = (current_xid + 1) % TOTAL_XID
    
    # 2. YENİ VERİ EKLEME (Rastgele aralıklarla)
    if frame % 50 == 0:
        rows.append({'id': current_xid, 'frozen': False})

    # --- GÖRSELLEŞTİRME ---
    
    # A. Mevcut XID (İşlem yapan imleç - Kırmızı Çizgi)
    theta_current = np.deg2rad(current_xid)
    ax.plot([theta_current, theta_current], [0, 1], color='red', linewidth=3, label='Current XID')
    
    # B. Geçmiş / Güvenli Bölge (Yeşil Alan - 2 Milyar işlem gerisi)
    # Current XID'den geriye doğru 180 derece
    theta_safe = np.linspace(theta_current - np.pi, theta_current, 100)
    ax.fill_between(theta_safe, 0, 1, color='green', alpha=0.1, label='Görünür Geçmiş')

    # C. Satırları Çiz
    for row in rows:
        xid = row['id']
        age = (current_xid - xid) % TOTAL_XID
        
        # Koordinat (Radyan cinsinden)
        theta = np.deg2rad(xid)
        
        # DURUM KONTROLÜ:
        # Eğer satır dondurulmuşsa (Frozen) -> Daima Güvenli (Mavi)
        if row['frozen']:
            color = 'blue'
            status = 'Frozen (Güvenli)'
            
        # Eğer yaş ufuk çizgisini (180 derece) geçmişse -> WRAPAROUND HATASI (Kırmızı)
        # PostgreSQL buradaki satırı "gelecekte" sanıp gizler.
        elif age > HALF_CYCLE:
            color = 'red' 
            status = 'KAYIP (Wraparound!)'
            # Görsel efekt: Kırmızı ve büyük nokta
            ax.scatter(theta, 0.8, c=color, s=100, edgecolors='black', zorder=5)
            continue 

        # Henüz dondurulmamış ama güvenli (Yeşil)
        else:
            color = 'green'
            status = 'Normal'
            
            # OTOMATİK FREEZE SİMÜLASYONU
            # Aşağıdaki satırı açarsanız Vacuum işlemi simüle edilir:
            if age > FREEZE_AGE: row['frozen'] = True
            
        ax.scatter(theta, 0.8, c=color, s=50, edgecolors='black')

    # Bilgi Başlığı
    plt.title(f"PostgreSQL Wraparound Simülasyonu\nCurrent XID: {current_xid}\n(Kırmızı Noktalar = Veri Kaybı)", pad=20)
    
    return ax,

ani = animation.FuncAnimation(fig, update, frames=np.arange(0, 1000), init_func=init, interval=50)
plt.legend(loc='lower left', bbox_to_anchor=(-0.1, -0.1))
plt.show()
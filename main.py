import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Struktur Data - Linked List & Queue", layout="wide", page_icon="📚")

# ═══════════════════════════════════════════════════════
# STRUKTUR DATA
# ═══════════════════════════════════════════════════════

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# ── Linked List: Playlist Musik ──
class Playlist:
    def __init__(self):
        self.head = None
        self.size = 0

    def tambah_lagu(self, lagu, posisi="akhir"):
        node_baru = Node(lagu)
        self.size += 1
        if self.head is None:
            self.head = node_baru
            return
        if posisi == "awal":
            node_baru.next = self.head
            self.head = node_baru
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node_baru

    def hapus_lagu(self, lagu):
        if self.head is None:
            return False
        if self.head.data == lagu:
            self.head = self.head.next
            self.size -= 1
            return True
        current = self.head
        while current.next:
            if current.next.data == lagu:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        return False

    def tampilkan(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

# ── Stack: Browser History ──
class BrowserHistory:
    def __init__(self, halaman_awal="https://google.com"):
        self.current = Node(halaman_awal)
        self.back_stack = []
        self.forward_stack = []

    def kunjungi(self, url):
        self.back_stack.append(self.current.data)
        self.forward_stack.clear()
        self.current = Node(url)

    def back(self):
        if not self.back_stack:
            return False
        self.forward_stack.append(self.current.data)
        self.current = Node(self.back_stack.pop())
        return True

    def forward(self):
        if not self.forward_stack:
            return False
        self.back_stack.append(self.current.data)
        self.current = Node(self.forward_stack.pop())
        return True

# ── Queue: Antrian Bank ──
class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def enqueue(self, data):
        node_baru = Node(data)
        if self.rear is None:
            self.front = self.rear = node_baru
        else:
            self.rear.next = node_baru
            self.rear = node_baru
        self.size += 1

    def dequeue(self):
        if self.front is None:
            return None
        data = self.front.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self.size -= 1
        return data

    def peek(self):
        return self.front.data if self.front else None

    def is_empty(self):
        return self.size == 0

    def tampilkan(self):
        result = []
        current = self.front
        while current:
            result.append(current.data)
            current = current.next
        return result


# ═══════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════

if "playlist" not in st.session_state:
    st.session_state.playlist = Playlist()
    for lagu in ["Shape of You - Ed Sheeran", "Blinding Lights - The Weeknd", "Stay - Justin Bieber"]:
        st.session_state.playlist.tambah_lagu(lagu)

if "browser" not in st.session_state:
    st.session_state.browser = BrowserHistory()

if "antrian" not in st.session_state:
    st.session_state.antrian = Queue()

if "nomor_urut" not in st.session_state:
    st.session_state.nomor_urut = 1

if "sedang_dilayani" not in st.session_state:
    st.session_state.sedang_dilayani = None

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

if "notif" not in st.session_state:
    st.session_state.notif = {"playlist": None, "browser": None, "bank": None}


# ═══════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════

st.markdown("""
<style>
    .block-container { padding: 1.5rem 2.5rem; }

    /* Header */
    .header-utama {
        background: linear-gradient(135deg, #1e1b4b, #3730a3);
        border-radius: 16px; padding: 1.5rem 2rem;
        margin-bottom: 1.5rem; color: white;
    }
    .header-utama h1 { margin: 0; font-size: 1.8rem; }
    .header-utama p  { margin: 0.2rem 0 0; opacity: 0.75; font-size: 0.9rem; }

    /* Kartu */
    .kartu {
        background: #f8faff; border: 1px solid #e2e8f0;
        border-radius: 14px; padding: 1.3rem; margin-bottom: 1rem;
    }
    .kartu-judul { font-size: 1rem; font-weight: 700; color: #1e293b; margin-bottom: 0.8rem; }
    .badge {
        display: inline-block; background: #eff6ff; color: #2563eb;
        border-radius: 5px; padding: 2px 8px; font-size: 0.72rem;
        font-weight: 600; margin-bottom: 0.8rem;
    }

    /* ── PLAYLIST ── */
    .item-lagu {
        display: flex; align-items: center; gap: 0.7rem;
        background: white; border: 1px solid #e2e8f0;
        border-radius: 8px; padding: 0.55rem 0.9rem;
        margin-bottom: 0.4rem; font-size: 0.88rem;
    }
    .nomor-lagu { color: #6366f1; font-weight: 800; min-width: 24px; }

    /* ── BROWSER ── */
    .url-bar {
        background: white; border: 2px solid #c7d2fe;
        border-radius: 20px; padding: 0.45rem 1.1rem;
        color: #4338ca; font-size: 0.9rem; font-family: monospace;
        margin: 0.7rem 0; text-align: center;
    }
    .item-riwayat {
        padding: 0.3rem 0.75rem; border-radius: 6px;
        margin-bottom: 0.25rem; font-size: 0.82rem; font-family: monospace;
    }
    .aktif   { background: #4f46e5; color: white; font-weight: 700; }
    .tidak-aktif { background: #f1f5f9; color: #64748b; }

    /* ── BANK ── */
    .header-bank {
        background: linear-gradient(135deg, #1a3a6b, #2563eb);
        border-radius: 12px; padding: 1.2rem 1.5rem;
        margin-bottom: 1rem; color: white;
    }
    .header-bank h2 { margin: 0; font-size: 1.3rem; }
    .header-bank p  { margin: 0.1rem 0 0; opacity: 0.75; font-size: 0.82rem; }

    .tiket {
        display: flex; align-items: center; gap: 0.7rem;
        background: white; border: 1.5px solid #bfdbfe;
        border-radius: 10px; padding: 0.6rem 0.9rem;
        margin-bottom: 0.4rem;
    }
    .tiket-nomor {
        background: #2563eb; color: white; border-radius: 7px;
        padding: 0.25rem 0.6rem; font-weight: 800; font-size: 0.9rem;
        min-width: 48px; text-align: center;
    }
    .tiket-pertama .tiket-nomor { background: #16a34a; }
    .tiket-nama  { font-weight: 600; color: #1e293b; font-size: 0.88rem; }
    .tiket-meta  { color: #64748b; font-size: 0.75rem; }

    .layanan-aktif {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7);
        border: 2px solid #16a34a; border-radius: 12px;
        padding: 1rem; text-align: center; margin-bottom: 0.8rem;
    }
    .layanan-nomor { font-size: 2.5rem; font-weight: 900; color: #15803d; line-height: 1; }
    .layanan-nama  { font-size: 1rem; font-weight: 600; color: #166534; margin-top: 0.2rem; }

    .stat-box {
        background: white; border: 1px solid #e2e8f0;
        border-radius: 10px; padding: 0.8rem; text-align: center;
    }
    .stat-angka { font-size: 1.8rem; font-weight: 800; color: #2563eb; }
    .stat-label { font-size: 0.75rem; color: #64748b; }

    /* Notifikasi */
    .notif-sukses {
        background: #f0fdf4; border: 1px solid #86efac; color: #166534;
        border-radius: 8px; padding: 0.45rem 0.9rem; font-size: 0.83rem; margin-bottom: 0.7rem;
    }
    .notif-info {
        background: #eff6ff; border: 1px solid #93c5fd; color: #1d4ed8;
        border-radius: 8px; padding: 0.45rem 0.9rem; font-size: 0.83rem; margin-bottom: 0.7rem;
    }
    .notif-gagal {
        background: #fef2f2; border: 1px solid #fca5a5; color: #b91c1c;
        border-radius: 8px; padding: 0.45rem 0.9rem; font-size: 0.83rem; margin-bottom: 0.7rem;
    }
    .kosong { text-align: center; padding: 1.5rem; color: #94a3b8; font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════

st.markdown("""
<div class="header-utama">
    <h1>📚 Struktur Data – Linked List & Queue</h1>
    <p>Studi Kasus: Playlist Musik · Browser History · Sistem Antrian Bank</p>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# TAB
# ═══════════════════════════════════════════════════════

tab1, tab2, tab3 = st.tabs(["🎵  Playlist Musik", "🌐  Browser History", "🏦  Antrian Bank"])


# ══════════════════════════════════════════════
# TAB 1 – PLAYLIST MUSIK
# ══════════════════════════════════════════════

with tab1:
    col_kiri, col_kanan = st.columns([1.2, 1])

    with col_kiri:
        st.markdown('<div class="kartu">', unsafe_allow_html=True)
        st.markdown('<div class="kartu-judul">➕ Tambah Lagu</div>', unsafe_allow_html=True)
        st.markdown('<span class="badge">Operasi: Insert Node</span>', unsafe_allow_html=True)

        nama_lagu = st.text_input("Nama lagu & artis", placeholder="Judul – Artis", key="input_lagu")
        posisi = st.radio("Tambahkan di:", ["Akhir playlist", "Awal playlist"], horizontal=True)

        if st.button("➕ Tambah Lagu", use_container_width=True, key="btn_tambah_lagu"):
            if nama_lagu.strip():
                pos = "akhir" if posisi == "Akhir playlist" else "awal"
                st.session_state.playlist.tambah_lagu(nama_lagu.strip(), pos)
                st.session_state.notif["playlist"] = ("sukses", f'"{nama_lagu}" ditambahkan ke {pos} playlist.')
                st.rerun()
            else:
                st.session_state.notif["playlist"] = ("gagal", "Nama lagu tidak boleh kosong.")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="kartu">', unsafe_allow_html=True)
        st.markdown('<div class="kartu-judul">🗑️ Hapus Lagu</div>', unsafe_allow_html=True)
        st.markdown('<span class="badge">Operasi: Delete Node</span>', unsafe_allow_html=True)

        daftar_lagu = st.session_state.playlist.tampilkan()
        if daftar_lagu:
            pilih_hapus = st.selectbox("Pilih lagu:", daftar_lagu, key="pilih_hapus")
            if st.button("🗑️ Hapus Lagu", use_container_width=True, key="btn_hapus_lagu"):
                st.session_state.playlist.hapus_lagu(pilih_hapus)
                st.session_state.notif["playlist"] = ("sukses", f'"{pilih_hapus}" berhasil dihapus.')
                st.rerun()
        else:
            st.info("Playlist kosong.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_kanan:
        st.markdown('<div class="kartu">', unsafe_allow_html=True)
        st.markdown('<div class="kartu-judul">🎶 Playlist Saat Ini</div>', unsafe_allow_html=True)
        st.markdown('<span class="badge">Visualisasi Linked List</span>', unsafe_allow_html=True)

        notif = st.session_state.notif["playlist"]
        if notif:
            tipe, pesan = notif
            kelas = "notif-sukses" if tipe == "sukses" else "notif-gagal"
            ikon = "✅" if tipe == "sukses" else "❌"
            st.markdown(f'<div class="{kelas}">{ikon} {pesan}</div>', unsafe_allow_html=True)
            st.session_state.notif["playlist"] = None

        lagu_list = st.session_state.playlist.tampilkan()
        if lagu_list:
            for i, lagu in enumerate(lagu_list, 1):
                panah = "→" if i < len(lagu_list) else "→ NULL"
                st.markdown(
                    f'<div class="item-lagu"><span class="nomor-lagu">{i}.</span>'
                    f'<span style="flex:1">{lagu}</span>'
                    f'<span style="color:#cbd5e1;font-size:0.75rem">{panah}</span></div>',
                    unsafe_allow_html=True)
            st.markdown(f"<br><small style='color:#94a3b8'>Total: <b>{st.session_state.playlist.size}</b> lagu</small>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="kosong">Belum ada lagu di playlist.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 2 – BROWSER HISTORY
# ══════════════════════════════════════════════

with tab2:
    col_kiri2, col_kanan2 = st.columns([1.2, 1])

    with col_kiri2:
        st.markdown('<div class="kartu">', unsafe_allow_html=True)
        st.markdown('<div class="kartu-judul">🧭 Navigasi Browser</div>', unsafe_allow_html=True)
        st.markdown('<span class="badge">Operasi: Stack Push/Pop</span>', unsafe_allow_html=True)

        browser = st.session_state.browser
        c1, c2 = st.columns(2)
        with c1:
            if st.button("◀ Back", use_container_width=True, disabled=not browser.back_stack, key="btn_back"):
                browser.back()
                st.session_state.notif["browser"] = ("sukses", f"Kembali ke: {browser.current.data}")
                st.rerun()
        with c2:
            if st.button("Forward ▶", use_container_width=True, disabled=not browser.forward_stack, key="btn_forward"):
                browser.forward()
                st.session_state.notif["browser"] = ("sukses", f"Maju ke: {browser.current.data}")
                st.rerun()

        st.markdown(f'<div class="url-bar">🌐 {browser.current.data}</div>', unsafe_allow_html=True)

        url_baru = st.text_input("Kunjungi URL:", placeholder="https://contoh.com", key="input_url")
        if st.button("🔍 Kunjungi", use_container_width=True, key="btn_kunjungi"):
            url = url_baru.strip()
            if url:
                if not url.startswith("http"):
                    url = "https://" + url
                browser.kunjungi(url)
                st.session_state.notif["browser"] = ("sukses", f"Mengunjungi: {url}")
                st.rerun()
            else:
                st.session_state.notif["browser"] = ("gagal", "URL tidak boleh kosong.")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_kanan2:
        st.markdown('<div class="kartu">', unsafe_allow_html=True)
        st.markdown('<div class="kartu-judul">📋 Riwayat Kunjungan</div>', unsafe_allow_html=True)
        st.markdown('<span class="badge">Visualisasi Stack</span>', unsafe_allow_html=True)

        notif2 = st.session_state.notif["browser"]
        if notif2:
            tipe, pesan = notif2
            kelas = "notif-sukses" if tipe == "sukses" else "notif-gagal"
            ikon = "✅" if tipe == "sukses" else "❌"
            st.markdown(f'<div class="{kelas}">{ikon} {pesan}</div>', unsafe_allow_html=True)
            st.session_state.notif["browser"] = None

        browser = st.session_state.browser
        if browser.forward_stack:
            st.markdown("<small style='color:#94a3b8'>🔵 Bisa Forward:</small>", unsafe_allow_html=True)
            for url in reversed(browser.forward_stack):
                st.markdown(f'<div class="item-riwayat tidak-aktif">⬆ {url}</div>', unsafe_allow_html=True)

        st.markdown("<small style='color:#94a3b8'>🟢 Halaman Aktif:</small>", unsafe_allow_html=True)
        st.markdown(f'<div class="item-riwayat aktif">▶ {browser.current.data}</div>', unsafe_allow_html=True)

        if browser.back_stack:
            st.markdown("<small style='color:#94a3b8'>🔴 Bisa Back:</small>", unsafe_allow_html=True)
            for url in reversed(browser.back_stack):
                st.markdown(f'<div class="item-riwayat tidak-aktif">⬇ {url}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 3 – ANTRIAN BANK
# ══════════════════════════════════════════════

with tab3:
    st.markdown("""
    <div class="header-bank">
        <h2>🏦 Sistem Antrian Bank</h2>
        <p>Simulasi antrian nasabah menggunakan struktur data Queue (FIFO)</p>
    </div>
    """, unsafe_allow_html=True)

    # Statistik
    cs1, cs2, cs3 = st.columns(3)
    with cs1:
        st.markdown(f'<div class="stat-box"><div class="stat-angka">{st.session_state.antrian.size}</div><div class="stat-label">Menunggu</div></div>', unsafe_allow_html=True)
    with cs2:
        dilayani = "Ada" if st.session_state.sedang_dilayani else "Kosong"
        warna = "#16a34a" if st.session_state.sedang_dilayani else "#94a3b8"
        st.markdown(f'<div class="stat-box"><div class="stat-angka" style="color:{warna}">{dilayani}</div><div class="stat-label">Loket Saat Ini</div></div>', unsafe_allow_html=True)
    with cs3:
        st.markdown(f'<div class="stat-box"><div class="stat-angka">{len(st.session_state.riwayat)}</div><div class="stat-label">Selesai Dilayani</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_b1, col_b2, col_b3 = st.columns([1, 1.2, 1])

    with col_b1:
        st.markdown('<div class="kartu">', unsafe_allow_html=True)
        st.markdown('<div class="kartu-judul">📝 Daftar Antrian</div>', unsafe_allow_html=True)
        st.markdown('<span class="badge">Operasi: Enqueue</span>', unsafe_allow_html=True)

        nama_nasabah = st.text_input("Nama Nasabah", placeholder="Masukkan nama...", key="input_nasabah")
        keperluan = st.selectbox("Keperluan", [
            "💰 Setor Tunai", "🏧 Tarik Tunai", "💳 Buka Rekening",
            "📋 Administrasi", "💸 Transfer", "❓ Informasi"
        ], key="input_keperluan")

        if st.button("🎫 Ambil Nomor Antrian", use_container_width=True, type="primary", key="btn_antrian"):
            if nama_nasabah.strip():
                nomor = f"A{st.session_state.nomor_urut:03d}"
                waktu = datetime.now().strftime("%H:%M")
                st.session_state.antrian.enqueue({
                    "nomor": nomor, "nama": nama_nasabah.strip(),
                    "keperluan": keperluan, "waktu": waktu
                })
                st.session_state.nomor_urut += 1
                st.session_state.notif["bank"] = ("sukses", f"Nomor antrian {nomor} berhasil diambil!")
                st.rerun()
            else:
                st.session_state.notif["bank"] = ("gagal", "Nama nasabah tidak boleh kosong.")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="kartu">', unsafe_allow_html=True)
        st.markdown('<div class="kartu-judul">🔔 Panggil Nasabah</div>', unsafe_allow_html=True)
        st.markdown('<span class="badge">Operasi: Dequeue</span>', unsafe_allow_html=True)

        if not st.session_state.antrian.is_empty():
            brkt = st.session_state.antrian.peek()
            st.markdown(f"<small style='color:#64748b'>Berikutnya: <b>{brkt['nomor']} – {brkt['nama']}</b></small><br><br>", unsafe_allow_html=True)

        if st.button("📢 Panggil Berikutnya", use_container_width=True,
                     disabled=st.session_state.antrian.is_empty(), key="btn_panggil"):
            nasabah = st.session_state.antrian.dequeue()
            if nasabah:
                if st.session_state.sedang_dilayani:
                    st.session_state.riwayat.append(st.session_state.sedang_dilayani)
                st.session_state.sedang_dilayani = nasabah
                st.session_state.notif["bank"] = ("info", f"Memanggil {nasabah['nomor']} – {nasabah['nama']}")
                st.rerun()

        if st.session_state.sedang_dilayani:
            if st.button("✅ Selesai Dilayani", use_container_width=True, key="btn_selesai"):
                st.session_state.riwayat.append(st.session_state.sedang_dilayani)
                st.session_state.sedang_dilayani = None
                st.session_state.notif["bank"] = ("sukses", "Nasabah selesai dilayani.")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b2:
        notif3 = st.session_state.notif["bank"]
        if notif3:
            tipe, pesan = notif3
            kelas = {"sukses": "notif-sukses", "info": "notif-info", "gagal": "notif-gagal"}[tipe]
            ikon  = {"sukses": "✅", "info": "🔔", "gagal": "❌"}[tipe]
            st.markdown(f'<div class="{kelas}">{ikon} {pesan}</div>', unsafe_allow_html=True)
            st.session_state.notif["bank"] = None

        st.markdown('<div class="kartu-judul">🏪 Loket Pelayanan</div>', unsafe_allow_html=True)
        if st.session_state.sedang_dilayani:
            n = st.session_state.sedang_dilayani
            st.markdown(f"""
            <div class="layanan-aktif">
                <div style="font-size:0.75rem;color:#4ade80;letter-spacing:1px">🟢 SEDANG DILAYANI</div>
                <div class="layanan-nomor">{n['nomor']}</div>
                <div class="layanan-nama">{n['nama']}</div>
                <div style="color:#4ade80;font-size:0.82rem;margin-top:0.2rem">{n['keperluan']}</div>
                <div style="color:#86efac;font-size:0.75rem">⏰ {n['waktu']}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="layanan-aktif" style="background:#f8fafc;border-color:#e2e8f0">
                <div style="font-size:2rem">🪑</div>
                <div style="color:#94a3b8;font-size:0.85rem">Loket kosong</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="kartu-judul" style="margin-top:0.5rem">👥 Daftar Antrian</div>', unsafe_allow_html=True)
        daftar = st.session_state.antrian.tampilkan()
        if daftar:
            for i, n in enumerate(daftar):
                kelas_tiket = "tiket tiket-pertama" if i == 0 else "tiket"
                label = " 🔜" if i == 0 else ""
                st.markdown(f"""
                <div class="{kelas_tiket}">
                    <div class="tiket-nomor">{n['nomor']}</div>
                    <div>
                        <div class="tiket-nama">{n['nama']}{label}</div>
                        <div class="tiket-meta">{n['keperluan']} · {n['waktu']}</div>
                    </div>
                </div>""", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="display:flex;gap:0.5rem;margin-top:0.7rem;font-size:0.75rem">
                <span style="background:#dcfce7;color:#16a34a;padding:2px 8px;border-radius:4px;font-weight:600">FRONT → {daftar[0]['nomor']}</span>
                <span style="color:#cbd5e1">·····</span>
                <span style="background:#dbeafe;color:#1d4ed8;padding:2px 8px;border-radius:4px;font-weight:600">REAR → {daftar[-1]['nomor']}</span>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="kosong">🎉 Tidak ada nasabah yang menunggu</div>', unsafe_allow_html=True)

    with col_b3:
        st.markdown('<div class="kartu">', unsafe_allow_html=True)
        st.markdown('<div class="kartu-judul">📋 Riwayat Pelayanan</div>', unsafe_allow_html=True)
        if st.session_state.riwayat:
            for item in reversed(st.session_state.riwayat):
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:0.5rem;padding:0.35rem 0.7rem;
                     background:#f1f5f9;border-radius:7px;margin-bottom:0.3rem;font-size:0.82rem;color:#475569">
                    <span style="background:#16a34a;color:white;border-radius:4px;
                          padding:1px 6px;font-size:0.72rem;font-weight:700">{item['nomor']}</span>
                    <span><b>{item['nama']}</b></span>
                </div>""", unsafe_allow_html=True)
            if st.button("🗑️ Hapus Riwayat", use_container_width=True, key="btn_hapus_riwayat"):
                st.session_state.riwayat = []
                st.rerun()
        else:
            st.markdown('<div class="kosong">Belum ada nasabah selesai dilayani.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="kartu">', unsafe_allow_html=True)
        st.markdown('<div class="kartu-judul">📖 Konsep Queue</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:0.8rem;color:#475569;line-height:1.7">
            <b>FIFO</b> — First In, First Out<br>
            Nasabah pertama datang = pertama dilayani.<br><br>
            <b>Enqueue</b> → Tambah ke <code>REAR</code><br>
            <b>Dequeue</b> → Ambil dari <code>FRONT</code><br>
            <b>Peek</b> → Lihat <code>FRONT</code> tanpa hapus<br><br>
            <code>FRONT→[A001]→[A002]→[A003]→REAR</code>
        </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

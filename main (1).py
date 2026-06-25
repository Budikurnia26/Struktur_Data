import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Struktur Data", layout="wide", page_icon="📚")

# ═══════════════════════════════════════════════════════
# STRUKTUR DATA
# ═══════════════════════════════════════════════════════

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class DoublyNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

# ── Linked List ──
class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def tambah(self, data, posisi="akhir"):
        node_baru = Node(data)
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

    def hapus(self, data):
        if self.head is None:
            return False
        if self.head.data == data:
            self.head = self.head.next
            self.size -= 1
            return True
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        return False

    def tampilkan(self):
        result, current = [], self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

# ── Queue ──
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
        result, current = [], self.front
        while current:
            result.append(current.data)
            current = current.next
        return result

# ── Stack (Browser History) ──
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

# ── Doubly Linked List (Undo/Redo) ──
class UndoRedoEditor:
    def __init__(self):
        self.current = DoublyNode("")
        self.head = self.current

    def ketik(self, teks):
        node_baru = DoublyNode(teks)
        node_baru.prev = self.current
        self.current.next = node_baru
        self.current = node_baru

    def undo(self):
        if self.current.prev:
            self.current = self.current.prev
            return True
        return False

    def redo(self):
        if self.current.next:
            self.current = self.current.next
            return True
        return False

    def teks_sekarang(self):
        return self.current.data

    def riwayat(self):
        result = []
        node = self.head
        while node:
            result.append(node.data)
            node = node.next
        return result


# ═══════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════

# SK1 – Playlist
if "playlist" not in st.session_state:
    st.session_state.playlist = LinkedList()
    for l in ["Shape of You - Ed Sheeran", "Blinding Lights - The Weeknd", "Stay - Justin Bieber"]:
        st.session_state.playlist.tambah(l)

# SK2 – Browser History
if "browser" not in st.session_state:
    st.session_state.browser = BrowserHistory()

# SK3 – Koperasi
if "koperasi" not in st.session_state:
    st.session_state.koperasi = LinkedList()
    for a in [{"nama": "Budi Santoso", "no": "K001", "jabatan": "Ketua"},
              {"nama": "Sari Dewi",    "no": "K002", "jabatan": "Anggota"}]:
        st.session_state.koperasi.tambah(a)

# SK4 – Reservasi Hotel
if "reservasi" not in st.session_state:
    st.session_state.reservasi = LinkedList()

if "no_reservasi" not in st.session_state:
    st.session_state.no_reservasi = 1

# SK5 – Antrian RS
if "antrian_rs" not in st.session_state:
    st.session_state.antrian_rs = Queue()

if "no_pasien" not in st.session_state:
    st.session_state.no_pasien = 1

if "dilayani_rs" not in st.session_state:
    st.session_state.dilayani_rs = None

if "riwayat_rs" not in st.session_state:
    st.session_state.riwayat_rs = []

# SK6 – Undo/Redo
if "editor" not in st.session_state:
    st.session_state.editor = UndoRedoEditor()

if "input_teks" not in st.session_state:
    st.session_state.input_teks = ""

# Antrian Bank (lama)
if "antrian" not in st.session_state:
    st.session_state.antrian = Queue()
if "nomor_urut" not in st.session_state:
    st.session_state.nomor_urut = 1
if "sedang_dilayani" not in st.session_state:
    st.session_state.sedang_dilayani = None
if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

# Notifikasi
if "notif" not in st.session_state:
    st.session_state.notif = {k: None for k in ["playlist","browser","koperasi","reservasi","rs","editor","bank"]}


# ═══════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════

st.markdown("""
<style>
    .block-container { padding: 1.5rem 2.5rem; }
    .header-utama {
        background: linear-gradient(135deg, #1e1b4b, #3730a3);
        border-radius: 16px; padding: 1.5rem 2rem; margin-bottom: 1.5rem; color: white;
    }
    .header-utama h1 { margin: 0; font-size: 1.8rem; }
    .header-utama p  { margin: 0.2rem 0 0; opacity: 0.75; font-size: 0.9rem; }
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
    .item-list {
        display: flex; align-items: center; gap: 0.7rem;
        background: white; border: 1px solid #e2e8f0;
        border-radius: 8px; padding: 0.55rem 0.9rem;
        margin-bottom: 0.4rem; font-size: 0.88rem;
    }
    .nomor { color: #6366f1; font-weight: 800; min-width: 24px; }
    .url-bar {
        background: white; border: 2px solid #c7d2fe;
        border-radius: 20px; padding: 0.45rem 1.1rem;
        color: #4338ca; font-size: 0.9rem; font-family: monospace;
        margin: 0.7rem 0; text-align: center;
    }
    .item-riwayat { padding: 0.3rem 0.75rem; border-radius: 6px; margin-bottom: 0.25rem; font-size: 0.82rem; font-family: monospace; }
    .aktif       { background: #4f46e5; color: white; font-weight: 700; }
    .tidak-aktif { background: #f1f5f9; color: #64748b; }
    .tiket {
        display: flex; align-items: center; gap: 0.7rem;
        background: white; border: 1.5px solid #bfdbfe;
        border-radius: 10px; padding: 0.6rem 0.9rem; margin-bottom: 0.4rem;
    }
    .tiket-nomor {
        background: #2563eb; color: white; border-radius: 7px;
        padding: 0.25rem 0.6rem; font-weight: 800; font-size: 0.9rem;
        min-width: 48px; text-align: center;
    }
    .tiket-pertama .tiket-nomor { background: #16a34a; }
    .tiket-nama { font-weight: 600; color: #1e293b; font-size: 0.88rem; }
    .tiket-meta { color: #64748b; font-size: 0.75rem; }
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
    .editor-box {
        background: white; border: 2px solid #e2e8f0; border-radius: 10px;
        padding: 1rem 1.2rem; font-size: 1rem; color: #1e293b;
        min-height: 80px; font-family: monospace; margin: 0.5rem 0;
        white-space: pre-wrap; word-break: break-word;
    }
    .riwayat-node {
        display: inline-block; background: #eff6ff; color: #1d4ed8;
        border: 1px solid #bfdbfe; border-radius: 6px;
        padding: 3px 10px; margin: 3px; font-size: 0.8rem; font-family: monospace;
    }
    .riwayat-node.aktif-node { background: #4f46e5; color: white; border-color: #4f46e5; font-weight: 700; }
    .notif-sukses { background:#f0fdf4;border:1px solid #86efac;color:#166534;border-radius:8px;padding:0.45rem 0.9rem;font-size:0.83rem;margin-bottom:0.7rem; }
    .notif-info   { background:#eff6ff;border:1px solid #93c5fd;color:#1d4ed8;border-radius:8px;padding:0.45rem 0.9rem;font-size:0.83rem;margin-bottom:0.7rem; }
    .notif-gagal  { background:#fef2f2;border:1px solid #fca5a5;color:#b91c1c;border-radius:8px;padding:0.45rem 0.9rem;font-size:0.83rem;margin-bottom:0.7rem; }
    .kosong { text-align:center;padding:1.5rem;color:#94a3b8;font-size:0.85rem; }
</style>
""", unsafe_allow_html=True)

def notif_html(key):
    n = st.session_state.notif[key]
    if n:
        tipe, pesan = n
        kelas = {"sukses":"notif-sukses","info":"notif-info","gagal":"notif-gagal"}[tipe]
        ikon  = {"sukses":"✅","info":"🔔","gagal":"❌"}[tipe]
        st.markdown(f'<div class="{kelas}">{ikon} {pesan}</div>', unsafe_allow_html=True)
        st.session_state.notif[key] = None

def set_notif(key, tipe, pesan):
    st.session_state.notif[key] = (tipe, pesan)


# ═══════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════

st.markdown("""
<div class="header-utama">
    <h1>📚 Struktur Data – Linked List & Queue</h1>
    <p>Studi Kasus 1–6 · Playlist · Browser History · Koperasi · Hotel · Rumah Sakit · Undo/Redo</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🎵 Playlist Musik",
    "🌐 Browser History",
    "🤝 Daftar Koperasi",
    "🏨 Reservasi Hotel",
    "🏥 Antrian RS",
    "↩️ Undo/Redo Editor"
])


# ══════════════════════════════════════════════
# TAB 1 – PLAYLIST MUSIK
# ══════════════════════════════════════════════

with tab1:
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown('<div class="kartu">', unsafe_allow_html=True)
        st.markdown('<div class="kartu-judul">➕ Tambah Lagu</div>', unsafe_allow_html=True)
        st.markdown('<span class="badge">Operasi: Insert Node</span>', unsafe_allow_html=True)
        nama_lagu = st.text_input("Nama lagu & artis", placeholder="Judul – Artis", key="in_lagu")
        posisi    = st.radio("Tambahkan di:", ["Akhir playlist", "Awal playlist"], horizontal=True, key="pos_lagu")
        if st.button("➕ Tambah Lagu", use_container_width=True, key="btn_tambah_lagu"):
            if nama_lagu.strip():
                pos = "akhir" if posisi == "Akhir playlist" else "awal"
                st.session_state.playlist.tambah(nama_lagu.strip(), pos)
                set_notif("playlist", "sukses", f'"{nama_lagu}" ditambahkan ke {pos} playlist.')
                st.rerun()
            else:
                set_notif("playlist", "gagal", "Nama lagu tidak boleh kosong.")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="kartu">', unsafe_allow_html=True)
        st.markdown('<div class="kartu-judul">🗑️ Hapus Lagu</div>', unsafe_allow_html=True)
        st.markdown('<span class="badge">Operasi: Delete Node</span>', unsafe_allow_html=True)
        daftar_lagu = st.session_state.playlist.tampilkan()
        if daftar_lagu:
            pilih = st.selectbox("Pilih lagu:", daftar_lagu, key="pilih_lagu")
            if st.button("🗑️ Hapus", use_container_width=True, key="btn_hapus_lagu"):
                st.session_state.playlist.hapus(pilih)
                set_notif("playlist", "sukses", f'"{pilih}" dihapus.')
                st.rerun()
        else:
            st.info("Playlist kosong.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="kartu">', unsafe_allow_html=True)
        st.markdown('<div class="kartu-judul">🎶 Playlist Saat Ini</div>', unsafe_allow_html=True)
        st.markdown('<span class="badge">Visualisasi Linked List</span>', unsafe_allow_html=True)
        notif_html("playlist")
        lagu_list = st.session_state.playlist.tampilkan()
        if lagu_list:
            for i, l in enumerate(lagu_list, 1):
                panah = "→" if i < len(lagu_list) else "→ NULL"
                st.markdown(f'<div class="item-list"><span class="nomor">{i}.</span><span style="flex:1">{l}</span><span style="color:#cbd5e1;font-size:0.75rem">{panah}</span></div>', unsafe_allow_html=True)
            st.markdown(f"<small style='color:#94a3b8'>Total: <b>{st.session_state.playlist.size}</b> lagu</small>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="kosong">Belum ada lagu.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 2 – BROWSER HISTORY
# ══════════════════════════════════════════════

with tab2:
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown('<div class="kartu">', unsafe_allow_html=True)
        st.markdown('<div class="kartu-judul">🧭 Navigasi Browser</div>', unsafe_allow_html=True)
        st.markdown('<span class="badge">Operasi: Stack Push/Pop</span>', unsafe_allow_html=True)
        browser = st.session_state.browser
        c1, c2 = st.columns(2)
        with c1:
            if st.button("◀ Back", use_container_width=True, disabled=not browser.back_stack, key="btn_back"):
                browser.back()
                set_notif("browser", "sukses", f"Kembali ke: {browser.current.data}")
                st.rerun()
        with c2:
            if st.button("Forward ▶", use_container_width=True, disabled=not browser.forward_stack, key="btn_fwd"):
                browser.forward()
                set_notif("browser", "sukses", f"Maju ke: {browser.current.data}")
                st.rerun()
        st.markdown(f'<div class="url-bar">🌐 {browser.current.data}</div>', unsafe_allow_html=True)
        url_baru = st.text_input("Kunjungi URL:", placeholder="https://contoh.com", key="in_url")
        if st.button("🔍 Kunjungi", use_container_width=True, key="btn_kunjungi"):
            url = url_baru.strip()
            if url:
                if not url.startswith("http"): url = "https://" + url
                browser.kunjungi(url)
                set_notif("browser", "sukses", f"Mengunjungi: {url}")
                st.rerun()
            else:
                set_notif("browser", "gagal", "URL tidak boleh kosong.")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="kartu">', unsafe_allow_html=True)
        st.markdown('<div class="kartu-judul">📋 Riwayat Kunjungan</div>', unsafe_allow_html=True)
        st.markdown('<span class="badge">Visualisasi Stack</span>', unsafe_allow_html=True)
        notif_html("browser")
        if browser.forward_stack:
            st.markdown("<small style='color:#94a3b8'>🔵 Bisa Forward:</small>", unsafe_allow_html=True)
            for u in reversed(browser.forward_stack):
                st.markdown(f'<div class="item-riwayat tidak-aktif">⬆ {u}</div>', unsafe_allow_html=True)
        st.markdown("<small style='color:#94a3b8'>🟢 Halaman Aktif:</small>", unsafe_allow_html=True)
        st.markdown(f'<div class="item-riwayat aktif">▶ {browser.current.data}</div>', unsafe_allow_html=True)
        if browser.back_stack:
            st.markdown("<small style='color:#94a3b8'>🔴 Bisa Back:</small>", unsafe_allow_html=True)
            for u in reversed(browser.back_stack):
                st.markdown(f'<div class="item-riwayat tidak-aktif">⬇ {u}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 3 – DAFTAR ANGGOTA KOPERASI
# ══════════════════════════════════════════════

with tab3:
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown('<div class="kartu">', unsafe_allow_html=True)
        st.markdown('<div class="kartu-judul">➕ Tambah Anggota</div>', unsafe_allow_html=True)
        st.markdown('<span class="badge">Operasi: Insert Node</span>', unsafe_allow_html=True)
        nama_anggota = st.text_input("Nama Anggota", placeholder="Nama lengkap", key="in_anggota")
        jabatan      = st.selectbox("Jabatan", ["Anggota", "Pengurus", "Ketua", "Bendahara", "Sekretaris"], key="in_jabatan")
        no_anggota   = f"K{(st.session_state.koperasi.size + 1):03d}"
        st.markdown(f"<small style='color:#64748b'>No. Anggota: <b>{no_anggota}</b></small>", unsafe_allow_html=True)
        if st.button("➕ Tambah Anggota", use_container_width=True, key="btn_tambah_kop"):
            if nama_anggota.strip():
                data = {"nama": nama_anggota.strip(), "no": no_anggota, "jabatan": jabatan}
                st.session_state.koperasi.tambah(data)
                set_notif("koperasi", "sukses", f"{nama_anggota} berhasil ditambahkan.")
                st.rerun()
            else:
                set_notif("koperasi", "gagal", "Nama tidak boleh kosong.")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="kartu">', unsafe_allow_html=True)
        st.markdown('<div class="kartu-judul">🗑️ Hapus Anggota</div>', unsafe_allow_html=True)
        st.markdown('<span class="badge">Operasi: Delete Node</span>', unsafe_allow_html=True)
        daftar_kop = st.session_state.koperasi.tampilkan()
        if daftar_kop:
            pilihan = [f"{a['no']} – {a['nama']}" for a in daftar_kop]
            pilih_kop = st.selectbox("Pilih anggota:", pilihan, key="pilih_kop")
            if st.button("🗑️ Hapus Anggota", use_container_width=True, key="btn_hapus_kop"):
                idx = pilihan.index(pilih_kop)
                target = daftar_kop[idx]
                st.session_state.koperasi.hapus(target)
                set_notif("koperasi", "sukses", f"{target['nama']} dihapus dari daftar.")
                st.rerun()
        else:
            st.info("Daftar anggota kosong.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="kartu">', unsafe_allow_html=True)
        st.markdown('<div class="kartu-judul">👥 Daftar Anggota Koperasi</div>', unsafe_allow_html=True)
        st.markdown('<span class="badge">Visualisasi Linked List</span>', unsafe_allow_html=True)
        notif_html("koperasi")
        daftar_kop = st.session_state.koperasi.tampilkan()
        if daftar_kop:
            for i, a in enumerate(daftar_kop, 1):
                panah = "→" if i < len(daftar_kop) else "→ NULL"
                st.markdown(f'''
                <div class="item-list">
                    <span class="nomor">{i}.</span>
                    <div style="flex:1">
                        <div style="font-weight:600;color:#1e293b">{a['nama']}</div>
                        <div style="font-size:0.75rem;color:#64748b">{a['no']} · {a['jabatan']}</div>
                    </div>
                    <span style="color:#cbd5e1;font-size:0.75rem">{panah}</span>
                </div>''', unsafe_allow_html=True)
            st.markdown(f"<small style='color:#94a3b8'>Total: <b>{st.session_state.koperasi.size}</b> anggota</small>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="kosong">Belum ada anggota.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 4 – RESERVASI HOTEL
# ══════════════════════════════════════════════

with tab4:
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown('<div class="kartu">', unsafe_allow_html=True)
        st.markdown('<div class="kartu-judul">🏨 Tambah Reservasi</div>', unsafe_allow_html=True)
        st.markdown('<span class="badge">Operasi: Insert Node</span>', unsafe_allow_html=True)
        nama_tamu   = st.text_input("Nama Tamu", placeholder="Nama lengkap tamu", key="in_tamu")
        tipe_kamar  = st.selectbox("Tipe Kamar", ["Standard", "Deluxe", "Suite", "Family Room"], key="in_kamar")
        col_cin, col_cout = st.columns(2)
        with col_cin:
            check_in  = st.date_input("Check-in",  key="in_checkin")
        with col_cout:
            check_out = st.date_input("Check-out", key="in_checkout")
        no_res = f"RSV{st.session_state.no_reservasi:03d}"
        st.markdown(f"<small style='color:#64748b'>No. Reservasi: <b>{no_res}</b></small>", unsafe_allow_html=True)
        if st.button("📋 Buat Reservasi", use_container_width=True, type="primary", key="btn_reservasi"):
            if nama_tamu.strip():
                if check_out > check_in:
                    durasi = (check_out - check_in).days
                    data = {
                        "no": no_res, "nama": nama_tamu.strip(),
                        "kamar": tipe_kamar, "check_in": str(check_in),
                        "check_out": str(check_out), "durasi": durasi
                    }
                    st.session_state.reservasi.tambah(data)
                    st.session_state.no_reservasi += 1
                    set_notif("reservasi", "sukses", f"Reservasi {no_res} atas nama {nama_tamu} berhasil dibuat.")
                    st.rerun()
                else:
                    set_notif("reservasi", "gagal", "Check-out harus setelah Check-in.")
                    st.rerun()
            else:
                set_notif("reservasi", "gagal", "Nama tamu tidak boleh kosong.")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="kartu">', unsafe_allow_html=True)
        st.markdown('<div class="kartu-judul">🗑️ Batalkan Reservasi</div>', unsafe_allow_html=True)
        st.markdown('<span class="badge">Operasi: Delete Node</span>', unsafe_allow_html=True)
        daftar_res = st.session_state.reservasi.tampilkan()
        if daftar_res:
            pilihan_res = [f"{r['no']} – {r['nama']}" for r in daftar_res]
            pilih_res   = st.selectbox("Pilih reservasi:", pilihan_res, key="pilih_res")
            if st.button("🗑️ Batalkan", use_container_width=True, key="btn_hapus_res"):
                idx = pilihan_res.index(pilih_res)
                target = daftar_res[idx]
                st.session_state.reservasi.hapus(target)
                set_notif("reservasi", "sukses", f"Reservasi {target['no']} dibatalkan.")
                st.rerun()
        else:
            st.info("Tidak ada reservasi.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="kartu">', unsafe_allow_html=True)
        st.markdown('<div class="kartu-judul">📋 Daftar Reservasi</div>', unsafe_allow_html=True)
        st.markdown('<span class="badge">Visualisasi Linked List</span>', unsafe_allow_html=True)
        notif_html("reservasi")
        daftar_res = st.session_state.reservasi.tampilkan()
        if daftar_res:
            for i, r in enumerate(daftar_res, 1):
                panah = "→" if i < len(daftar_res) else "→ NULL"
                st.markdown(f'''
                <div class="item-list">
                    <span class="nomor">{i}.</span>
                    <div style="flex:1">
                        <div style="font-weight:600;color:#1e293b">{r['nama']} <span style="font-size:0.75rem;color:#6366f1">[{r['no']}]</span></div>
                        <div style="font-size:0.75rem;color:#64748b">{r['kamar']} · {r['check_in']} s/d {r['check_out']} ({r['durasi']} malam)</div>
                    </div>
                    <span style="color:#cbd5e1;font-size:0.75rem">{panah}</span>
                </div>''', unsafe_allow_html=True)
            st.markdown(f"<small style='color:#94a3b8'>Total: <b>{st.session_state.reservasi.size}</b> reservasi</small>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="kosong">Belum ada reservasi.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 5 – ANTRIAN RUMAH SAKIT
# ══════════════════════════════════════════════

with tab5:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#164e63,#0891b2);border-radius:12px;
         padding:1.2rem 1.5rem;margin-bottom:1rem;color:white">
        <h2 style="margin:0;font-size:1.3rem">🏥 Sistem Antrian Rumah Sakit</h2>
        <p style="margin:0.1rem 0 0;opacity:0.75;font-size:0.82rem">Pasien baru ditambahkan secara dinamis menggunakan Queue (FIFO)</p>
    </div>""", unsafe_allow_html=True)

    cs1, cs2, cs3 = st.columns(3)
    with cs1:
        st.markdown(f'<div class="stat-box"><div class="stat-angka">{st.session_state.antrian_rs.size}</div><div class="stat-label">Menunggu</div></div>', unsafe_allow_html=True)
    with cs2:
        ada = "Ada" if st.session_state.dilayani_rs else "Kosong"
        warna = "#16a34a" if st.session_state.dilayani_rs else "#94a3b8"
        st.markdown(f'<div class="stat-box"><div class="stat-angka" style="color:{warna}">{ada}</div><div class="stat-label">Ruang Periksa</div></div>', unsafe_allow_html=True)
    with cs3:
        st.markdown(f'<div class="stat-box"><div class="stat-angka">{len(st.session_state.riwayat_rs)}</div><div class="stat-label">Selesai</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col1:
        st.markdown('<div class="kartu">', unsafe_allow_html=True)
        st.markdown('<div class="kartu-judul">🩺 Daftar Pasien</div>', unsafe_allow_html=True)
        st.markdown('<span class="badge">Operasi: Enqueue</span>', unsafe_allow_html=True)
        nama_pasien = st.text_input("Nama Pasien", placeholder="Nama lengkap", key="in_pasien")
        poli        = st.selectbox("Poli Tujuan", ["Umum", "Anak", "Kandungan", "Gigi", "Mata", "Bedah", "Jantung"], key="in_poli")
        keluhan     = st.text_input("Keluhan", placeholder="Keluhan singkat", key="in_keluhan")
        if st.button("🎫 Ambil Nomor Antrian", use_container_width=True, type="primary", key="btn_antrian_rs"):
            if nama_pasien.strip():
                no = f"P{st.session_state.no_pasien:03d}"
                waktu = datetime.now().strftime("%H:%M")
                st.session_state.antrian_rs.enqueue({
                    "no": no, "nama": nama_pasien.strip(),
                    "poli": poli, "keluhan": keluhan, "waktu": waktu
                })
                st.session_state.no_pasien += 1
                set_notif("rs", "sukses", f"Nomor antrian {no} berhasil diambil!")
                st.rerun()
            else:
                set_notif("rs", "gagal", "Nama pasien tidak boleh kosong.")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="kartu">', unsafe_allow_html=True)
        st.markdown('<div class="kartu-judul">🔔 Panggil Pasien</div>', unsafe_allow_html=True)
        st.markdown('<span class="badge">Operasi: Dequeue</span>', unsafe_allow_html=True)
        if not st.session_state.antrian_rs.is_empty():
            brkt = st.session_state.antrian_rs.peek()
            st.markdown(f"<small style='color:#64748b'>Berikutnya: <b>{brkt['no']} – {brkt['nama']}</b></small><br><br>", unsafe_allow_html=True)
        if st.button("📢 Panggil Pasien", use_container_width=True,
                     disabled=st.session_state.antrian_rs.is_empty(), key="btn_panggil_rs"):
            pasien = st.session_state.antrian_rs.dequeue()
            if pasien:
                if st.session_state.dilayani_rs:
                    st.session_state.riwayat_rs.append(st.session_state.dilayani_rs)
                st.session_state.dilayani_rs = pasien
                set_notif("rs", "info", f"Memanggil {pasien['no']} – {pasien['nama']}")
                st.rerun()
        if st.session_state.dilayani_rs:
            if st.button("✅ Selesai Periksa", use_container_width=True, key="btn_selesai_rs"):
                st.session_state.riwayat_rs.append(st.session_state.dilayani_rs)
                st.session_state.dilayani_rs = None
                set_notif("rs", "sukses", "Pasien selesai diperiksa.")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        notif_html("rs")
        st.markdown('<div class="kartu-judul">🏥 Ruang Periksa</div>', unsafe_allow_html=True)
        if st.session_state.dilayani_rs:
            p = st.session_state.dilayani_rs
            st.markdown(f"""
            <div class="layanan-aktif">
                <div style="font-size:0.75rem;color:#4ade80;letter-spacing:1px">🟢 SEDANG DIPERIKSA</div>
                <div class="layanan-nomor">{p['no']}</div>
                <div class="layanan-nama">{p['nama']}</div>
                <div style="color:#4ade80;font-size:0.82rem;margin-top:0.2rem">Poli {p['poli']}</div>
                <div style="color:#86efac;font-size:0.75rem">{p['keluhan']} · ⏰ {p['waktu']}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="layanan-aktif" style="background:#f8fafc;border-color:#e2e8f0">
                <div style="font-size:2rem">🩺</div>
                <div style="color:#94a3b8;font-size:0.85rem">Ruang periksa kosong</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="kartu-judul" style="margin-top:0.5rem">👥 Antrian Pasien</div>', unsafe_allow_html=True)
        daftar_p = st.session_state.antrian_rs.tampilkan()
        if daftar_p:
            for i, p in enumerate(daftar_p):
                kelas = "tiket tiket-pertama" if i == 0 else "tiket"
                label = " 🔜" if i == 0 else ""
                st.markdown(f"""
                <div class="{kelas}">
                    <div class="tiket-nomor">{p['no']}</div>
                    <div>
                        <div class="tiket-nama">{p['nama']}{label}</div>
                        <div class="tiket-meta">Poli {p['poli']} · {p['waktu']}</div>
                    </div>
                </div>""", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="display:flex;gap:0.5rem;margin-top:0.7rem;font-size:0.75rem">
                <span style="background:#dcfce7;color:#16a34a;padding:2px 8px;border-radius:4px;font-weight:600">FRONT → {daftar_p[0]['no']}</span>
                <span style="color:#cbd5e1">·····</span>
                <span style="background:#dbeafe;color:#1d4ed8;padding:2px 8px;border-radius:4px;font-weight:600">REAR → {daftar_p[-1]['no']}</span>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="kosong">🎉 Tidak ada pasien yang menunggu</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="kartu">', unsafe_allow_html=True)
        st.markdown('<div class="kartu-judul">📋 Riwayat</div>', unsafe_allow_html=True)
        if st.session_state.riwayat_rs:
            for item in reversed(st.session_state.riwayat_rs):
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:0.5rem;padding:0.35rem 0.7rem;
                     background:#f1f5f9;border-radius:7px;margin-bottom:0.3rem;font-size:0.82rem">
                    <span style="background:#0891b2;color:white;border-radius:4px;
                          padding:1px 6px;font-size:0.72rem;font-weight:700">{item['no']}</span>
                    <span><b>{item['nama']}</b> · {item['poli']}</span>
                </div>""", unsafe_allow_html=True)
            if st.button("🗑️ Hapus Riwayat", use_container_width=True, key="btn_hapus_riwayat_rs"):
                st.session_state.riwayat_rs = []
                st.rerun()
        else:
            st.markdown('<div class="kosong">Belum ada pasien selesai.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 6 – UNDO/REDO EDITOR
# ══════════════════════════════════════════════

with tab6:
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown('<div class="kartu">', unsafe_allow_html=True)
        st.markdown('<div class="kartu-judul">✏️ Editor Teks</div>', unsafe_allow_html=True)
        st.markdown('<span class="badge">Struktur: Doubly Linked List</span>', unsafe_allow_html=True)

        teks_input = st.text_area("Ketik teks baru:", placeholder="Ketik sesuatu lalu klik Simpan...",
                                   height=100, key="in_editor")

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("💾 Simpan", use_container_width=True, key="btn_simpan"):
                if teks_input.strip():
                    st.session_state.editor.ketik(teks_input.strip())
                    set_notif("editor", "sukses", "Teks disimpan.")
                    st.rerun()
                else:
                    set_notif("editor", "gagal", "Teks tidak boleh kosong.")
                    st.rerun()
        with c2:
            bisa_undo = st.session_state.editor.current.prev is not None
            if st.button("↩️ Undo", use_container_width=True, disabled=not bisa_undo, key="btn_undo"):
                st.session_state.editor.undo()
                set_notif("editor", "info", "Undo berhasil.")
                st.rerun()
        with c3:
            bisa_redo = st.session_state.editor.current.next is not None
            if st.button("↪️ Redo", use_container_width=True, disabled=not bisa_redo, key="btn_redo"):
                st.session_state.editor.redo()
                set_notif("editor", "info", "Redo berhasil.")
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="kartu">', unsafe_allow_html=True)
        st.markdown('<div class="kartu-judul">📖 Konsep Doubly Linked List</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:0.8rem;color:#475569;line-height:1.8">
            Setiap node punya pointer <b>prev</b> dan <b>next</b>.<br>
            <b>Undo</b> → geser ke node <code>prev</code><br>
            <b>Redo</b> → geser ke node <code>next</code><br>
            <b>Simpan baru</b> → buat node baru di sebelah kanan<br><br>
            <code>NULL ← [v1] ⇄ [v2] ⇄ [v3] → NULL</code><br>
            <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↑ current</code>
        </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="kartu">', unsafe_allow_html=True)
        st.markdown('<div class="kartu-judul">📄 Teks Saat Ini</div>', unsafe_allow_html=True)
        notif_html("editor")
        teks_now = st.session_state.editor.teks_sekarang()
        if teks_now:
            st.markdown(f'<div class="editor-box">{teks_now}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="editor-box" style="color:#94a3b8;font-style:italic">Editor kosong...</div>', unsafe_allow_html=True)

        st.markdown('<div class="kartu-judul" style="margin-top:1rem">🔗 Visualisasi Node</div>', unsafe_allow_html=True)
        riwayat_editor = st.session_state.editor.riwayat()
        if len(riwayat_editor) > 1:
            html_nodes = ""
            for i, r in enumerate(riwayat_editor):
                label = r[:15] + "..." if len(r) > 15 else r
                label = label if label else "(kosong)"
                is_aktif = r == teks_now
                kelas = "riwayat-node aktif-node" if is_aktif else "riwayat-node"
                html_nodes += f'<span class="{kelas}">{label}</span>'
                if i < len(riwayat_editor) - 1:
                    html_nodes += '<span style="color:#94a3b8;font-size:0.8rem"> ⇄ </span>'
            st.markdown(f'<div style="margin-top:0.5rem;line-height:2.5">{html_nodes}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="kosong">Simpan beberapa versi untuk melihat node.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

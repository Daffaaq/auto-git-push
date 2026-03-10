import subprocess
import os
from datetime import datetime
from shutil import which

# ======================
# Helper functions
# ======================
def run(cmd):
    """Jalankan command shell, error kalau gagal"""
    subprocess.run(cmd, check=True)

def run_output(cmd):
    """Jalankan command dan kembalikan stdout"""
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

def check_gh():
    """Cek apakah GitHub CLI tersedia di PATH"""
    if not which("gh"):
        print("❌ GitHub CLI tidak ditemukan. Pastikan 'gh' ada di PATH")
        exit()

# ======================
# Git Init & Commit
# ======================
def check_git():
    """Inisialisasi git kalau belum ada"""
    if not os.path.exists(".git"):
        print("📦 Git belum diinisialisasi, menjalankan git init...")
        run(["git", "init"])

def initial_commit_if_needed():
    """Buat initial commit kalau belum ada commit sama sekali"""
    try:
        log = run_output(["git", "log", "--oneline"])
    except:
        log = ""
    if not log:
        print("📝 Membuat initial commit...")
        # Kalau folder kosong, buat README.md
        if not os.listdir("."):
            repo_name = os.path.basename(os.getcwd())
            with open("README.md", "w") as f:
                f.write(f"# {repo_name}\nAuto-generated README\n")
        # Buat .gitignore default PHP
        if not os.path.exists(".gitignore"):
            with open(".gitignore", "w") as f:
                f.write("vendor/\n.env\n*.log\n")
        run(["git", "add", "."])
        run(["git", "commit", "-m", "Initial commit"])
        print("✅ Initial commit berhasil dibuat")

# ======================
# GitHub Repo
# ======================
def check_remote():
    """Cek remote origin, buat repo GitHub kalau belum ada"""
    remotes = run_output(["git", "remote"])
    default_repo_name = os.path.basename(os.getcwd())

    if "origin" not in remotes:
        # Input nama repo
        repo_name = input(f"Masukkan nama repository GitHub (default: {default_repo_name}): ").strip()
        if not repo_name:
            repo_name = default_repo_name

        # Visibility
        visibility = input("Visibility repo? [public/private] (default: public): ").strip().lower()
        if visibility not in ["public", "private"]:
            visibility = "public"

        # Branch
        branch = input("Nama branch default (kosong = main): ").strip()
        if not branch:
            branch = "main"

        print(f"🚀 Membuat repository GitHub: {repo_name}")
        # Pastikan ada initial commit
        initial_commit_if_needed()
        # Create repo
        run(["gh", "repo", "create", repo_name,
             f"--{visibility}", "--source=.", "--remote=origin", "--push", "--confirm"])
        # Pastikan branch sesuai
        run(["git", "branch", "-M", branch])
        print(f"✅ Repository GitHub '{repo_name}' berhasil dibuat dan branch '{branch}' siap push")

# ======================
# Commit & Push
# ======================
def commit_push():
    """Commit perubahan lokal dan push ke GitHub"""
    status = run_output(["git", "status", "--porcelain"])
    if not status:
        print("⚠️ Tidak ada perubahan")
        return

    print("\n📄 Perubahan:\n")
    print(status)

    msg = input("\nMasukkan pesan commit (kosong = auto): ").strip()
    if not msg:
        msg = "auto commit " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    run(["git", "add", "."])
    run(["git", "commit", "-m", msg])

    branch = run_output(["git", "branch", "--show-current"])
    if not branch:
        branch = "main"
        run(["git", "branch", "-M", branch])

    # Pilih push atau skip
    do_push = input("Push sekarang ke GitHub? (y/n, default y): ").strip().lower()
    if do_push != "n":
        print(f"\n🚀 Push ke branch {branch}")
        run(["git", "push", "-u", "origin", branch])
        print("🎉 Push berhasil")

    # Logging
    with open("git_auto.log", "a") as log_file:
        log_file.write(f"{datetime.now()} | Commit: {msg} | Branch: {branch}\n")

# ======================
# Main
# ======================
def main():
    print("\n==== AUTO GIT TOOL V6 ====\n")
    check_gh()
    check_git()
    check_remote()
    commit_push()

if __name__ == "__main__":
    main()
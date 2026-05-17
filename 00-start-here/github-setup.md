# 🐙 GitHub Setup

> **Time needed**: 10 minutes
> **Why**: GitHub is where you'll commit your lab solutions, deploy CI/CD pipelines in Week 3, and show your portfolio to employers.

If you've used GitHub before, skim this and check off what's done. If you're new, work through it step by step.

---

## 🚀 Step-by-step

### 1. Create your GitHub account

- Go to [github.com](https://github.com)
- Click **Sign up**
- Use a professional username if possible — it shows up on your CV
  - ✅ Good: `shadrack-darku`, `kwameansah-dev`, `akosi-cloud`
  - ❌ Avoid: `xXcoolDude2010Xx`, `unicorn99`, `cypress777`
- Verify your email
- **Pick the free plan** — it's all you need

### 2. Choose a profile picture (optional, but recommended)

Recruiters will see your GitHub. A professional headshot or a clean avatar goes a long way.

### 3. Star this repo

Visit [the cloudwithshad-bootcamp repo](https://github.com/cloudwithshad/cloudwithshad-bootcamp-may2026) and click the **⭐ Star** button (top right). This bookmarks it AND helps other West Africans discover the bootcamp.

### 4. Fork the repo

Click **Fork** (top right of the repo) → it creates a copy under your own username. **You'll push your lab solutions to your fork**, not the original.

---

## 🔐 Set up Git locally

You need Git installed on your laptop so you can `git clone`, `git commit`, `git push`. If you already have it, just configure your name + email.

### Install Git

| OS | Command |
|----|---------|
| **macOS** | `git` should already exist. Confirm with `git --version`. If not: `brew install git` |
| **Windows** | Download [Git for Windows](https://git-scm.com/download/win). During install, **tick "Git Bash"** — that's the terminal you'll use |
| **Linux** | `sudo apt install git` (Ubuntu/Debian) or `sudo yum install git` (Amazon Linux) |

### Configure Git

Open Terminal (Mac/Linux) or Git Bash (Windows):

```bash
git config --global user.name "Your Real Name"
git config --global user.email "your-real-email@gmail.com"
```

> 💡 Use the **same email** as your GitHub account.

---

## 🔑 SSH key setup (recommended — saves typing passwords)

GitHub no longer accepts passwords for git push. You need either:
- A **Personal Access Token** (PAT) — easier but expires
- An **SSH key** — more setup but works forever

We recommend SSH. Here's how:

### 1. Generate the key

```bash
ssh-keygen -t ed25519 -C "your-email@gmail.com"
```

Press Enter to accept the default location. Pick a passphrase or leave blank.

### 2. Copy the public key

```bash
# macOS:
cat ~/.ssh/id_ed25519.pub | pbcopy

# Linux:
cat ~/.ssh/id_ed25519.pub
# (manually select and copy the output)

# Windows (Git Bash):
cat ~/.ssh/id_ed25519.pub | clip
```

### 3. Add it to GitHub

- Go to [GitHub → Settings → SSH and GPG keys](https://github.com/settings/keys)
- Click **New SSH key**
- Title: `My laptop` (or whatever)
- Paste the key
- Click **Add SSH key**

### 4. Test it

```bash
ssh -T git@github.com
```

Should respond: `Hi YOUR-USERNAME! You've successfully authenticated...`

---

## 📂 Clone your fork

Once you've forked this repo:

```bash
cd ~/Documents      # or wherever you keep code
git clone git@github.com:YOUR-USERNAME/cloudwithshad-bootcamp-may2026.git
cd cloudwithshad-bootcamp-may2026
```

Now you have a local copy you can edit and push to.

---

## 🔄 How to sync with the original repo

Every Friday, new content lands in the original repo (`cloudwithshad/cloudwithshad-bootcamp-may2026`). To pull the new week into your fork:

### One-time setup

```bash
# Add the original repo as an "upstream" remote
git remote add upstream https://github.com/cloudwithshad/cloudwithshad-bootcamp-may2026.git

# Verify both remotes are set
git remote -v
# origin    git@github.com:YOUR-USERNAME/...  (fetch)
# upstream  https://github.com/cloudwithshad/...  (fetch)
```

### Every Friday

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

You now have the new week's content in your local repo and your GitHub fork. 🎉

---

## 🎯 Your weekly habit

Treat your fork like your personal cloud journal:

| When | What |
|------|------|
| **Friday evening** | `git fetch upstream && git merge upstream/main` to get the new week |
| **Saturday** | Attend the live session, follow along |
| **Sun-Thu** | Do the labs, commit your solutions to a `my-solutions/` folder |
| **Friday** | Push to your fork: `git push origin main` |

The commit history of your fork becomes proof to employers that you put in the work. Recruiters DO look at GitHub activity.

---

## 💼 Make your GitHub profile employer-ready

Quick wins (5 minutes each):

1. **Bio**: "Aspiring Cloud Engineer · AWS Certified soon · cloudwithshad bootcamp May 2026"
2. **Pinned repos**: pin this fork once you've completed Week 1
3. **README profile**: create a special repo named `YOUR-USERNAME/YOUR-USERNAME` with a markdown file — it shows up at the top of your profile

See [`shared-resources/`](../shared-resources/) for more tips (additional guides coming soon).

---

## ✅ You're done when...

- [ ] You have a GitHub account
- [ ] Git is installed locally with your name + email configured
- [ ] You've starred + forked this repo
- [ ] You can `git clone` your fork to your laptop
- [ ] You can `ssh -T git@github.com` and get the "successfully authenticated" message

---

⬅️ [Back to Start Here](./README.md)

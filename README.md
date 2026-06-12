# CI/CD for Testing — Beginner Guide + Demo Project (June 2026)

> Banaya for Ranu — QA Engineer @ HawkVision AI.
> Theme: detection-metrics module (Precision/Recall/F1) taaki CI/CD seekhna
> aapke actual AI/CV QA kaam se connect ho jaaye.

---

## Part 0 — Sabse pehle: yeh project me kya-kya hai

```
cicd-demo/
├── detection_metrics.py        # chhota app code (validate events + confusion matrix)
├── test_detection_metrics.py   # 8 pytest tests
├── requirements.txt            # dependencies (pytest, coverage, ruff)
└── .github/
    └── workflows/
        └── ci.yml              # AAPKI PEHLI CI PIPELINE
```

Saare 8 tests pass hote hain aur lint clean hai — verified.

---

## Part 1 — Theory (sirf utni jitni zaroori hai)

### CI/CD kya hai, ek line me
- **CI = Continuous Integration:** har baar code push ho, machine *automatically*
  tests + lint chala kar bataye ki kuch toota to nahi.
- **CD = Continuous Delivery/Deployment:** tests pass hone ke baad code
  automatically staging/production tak pohonch jaaye.

QA ke liye sabse important hissa **CI** hai — kyunki tests yahin chalte hain.

### Kyun matter karta hai (QA ke perspective se)
Aap manually test karti hain, theek hai. Lekin jab team roz 10 baar code
push karti hai, to har baar manually sab kuch test karna impossible hai.
CI woh "robot QA" hai jo har commit par aapke likhe tests turant chala deta hai.
Toota hua code `main` branch tak pohonchne se *pehle* pakda jaata hai.

> 2026 reality: Senior/SDET job descriptions me ab "CI/CD pipeline design"
> ek *required* skill hai — sirf test likhna nahi. Yahi cheez "test likhne
> wale" aur "quality pipeline own karne wale" engineer me farak laati hai.
> **Yeh exactly aapka roadmap gap hai.**

### 5 building blocks (yeh 5 shabd yaad rakhein — bas itna kaafi hai shuru me)
| Term | Matlab |
|------|--------|
| **Workflow** | Ek YAML file (`.github/workflows/` me) jo batati hai *kab* aur *kya* chalega |
| **Trigger** | Event jo workflow start kare — sabse common: `push`, `pull_request` |
| **Job** | Kaam ka ek unit (jaise "test job"). Ek workflow me kai jobs ho sakte hain |
| **Step** | Job ke andar ek chhota action (checkout, install, test) |
| **Runner** | Woh virtual machine jahan job chalti hai (GitHub deta hai, free tier me) |

### Pipeline ki typical stages (sequence yaad rakho)
```
Lint  →  Test  →  Build  →  Security scan  →  Deploy (staging)  →  Deploy (prod, approval ke baad)
```
QA ke liye pehli 2 stages (**Lint + Test**) sabse zaroori. Baaki baad me.

### Free hai kya?
Haan. Public repo ke liye GitHub Actions free hai; private repo me free tier
me bhi acche khaase minutes milte hain. Seekhne ke liye ek **public repo**
bana lo — zero cost.

---

## Part 2 — Step-by-step: demo ko live karein (~20 min)

### Step 1 — GitHub par naya repo banao
1. GitHub par jao → **New repository**
2. Naam: `cicd-demo` → **Public** rakho → Create.

### Step 2 — Yeh project files upload karo
Option A (simple): GitHub UI par "Add file → Upload files" se saari files daalo.
Dhyan rakho `.github/workflows/ci.yml` ka folder structure bana rahe — UI me
file ka naam `.github/workflows/ci.yml` likh do, folders khud ban jaayenge.

Option B (terminal se — recommended, Git practice ho jaayega):
```bash
cd cicd-demo
git init
git add .
git commit -m "Initial commit: detection metrics + CI pipeline"
git branch -M main
git remote add origin https://github.com/<aapka-username>/cicd-demo.git
git push -u origin main
```

### Step 3 — Pipeline ko chalte hue dekho
- Repo me **Actions** tab kholo.
- Push ke saath hi "CI" workflow chalna shuru ho jaayega.
- Andar jaake har step (checkout → install → lint → test) green hote dekho.
- **Yeh moment important hai** — pehli baar aapne quality automate ki. 🎯

### Step 4 — Ab jaan-boojh kar fail karao (sabse zaroori learning)
1. `detection_metrics.py` me `validate_event` ke andar confidence check tod do
   (jaise `0.0 <= event.confidence <= 1.0` ko `0.0 <= event.confidence <= 2.0`).
2. Push karo.
3. Actions tab me **RED cross** dikhega, aur test log me exact line milegi jo fail hui.
4. Wapas theek karke push karo → green.

> Yahi CI ka asli faayda hai: galti *production se pehle* pakdi gayi.

### Step 5 — Branch protection ON karo (real-world workflow)
- Repo **Settings → Branches → Add rule** → branch `main`.
- "Require status checks to pass before merging" tick karo → CI select karo.
- Ab koi bhi PR tab tak merge nahi hoga jab tak tests green na ho.
- **Yeh woh setup hai jo har professional team use karti hai.**

---

## Part 3 — Apne actual product ko test karna (HawkVision wala kaam)

Demo ke baad asli sawaal: *apne product par yeh kaise lagayein?*

### A. Pehle decide karo kya-kya automate ho sakta hai
| Aapka manual test | CI me kaise aata hai |
|---|---|
| Detection accuracy (Precision/Recall/F1) | Ground-truth dataset par script chala kar threshold check karo (jaise F1 ≥ 0.85) |
| Alert payload validation (camera ID, timestamp, clip window) | API/JSON schema test — bilkul demo ke `validate_event` jaisa |
| RTSP stream up/health check | Smoke test job jo stream reachable hai ya nahi check kare |
| UI/dashboard flows | Playwright tests (aap pehle se explore kar rahi hain) |

### B. Suggested pipeline aapke product ke liye
```
Lint  →  Unit tests (metrics, validators)  →  Playwright E2E (dashboard)  →  Detection-accuracy gate
```
**Detection-accuracy gate** = ek custom job jo aapke model output ko
ground truth se compare kare aur F1 ek threshold se neeche ho to pipeline
ko FAIL kar de. Yeh aapke environment me **sabse strong differentiator**
hai — bahut kam QA log isko CI me daal paate hain.

### C. Practical adoption order (overwhelm mat ho)
1. Sirf unit tests CI me daalo (1 din ka kaam).
2. Lint add karo.
3. Playwright E2E ek alag job me add karo.
4. Phir detection-accuracy gate banao.
5. Last me deployment/CD.

Ek-ek karke. Sab ek saath nahi.

---

## Part 4 — AI angle (aapne yeh khaaskar poocha)

2026 me AI ne testing ko kaafi badal diya hai. Important: **AI Playwright/QA
ko replace nahi kar raha — augment kar raha hai.** Fundamentals abhi bhi zaroori
hain (warna AI ka generate kiya test review kaun karega?).

3 cheezein jo abhi relevant hain aapke liye:

1. **AI test generation** — plain English se Playwright tests generate karna.
   Locator priority yaad rakho: `getByRole > getByLabel > getByTestId > getByText > CSS`.
   AI ka output ~80% sahi hota hai; baaki aapko refine karna padta hai.

2. **Self-healing tests** — jab koi selector toot jaata hai (button ID badal gaya),
   AI usse automatically detect karke working replacement suggest/apply kar deta hai.
   Yeh "maintenance trap" (har sprint me aadhe tests flaky) ko kam karta hai.
   Playwright 1.56 (late 2025) ke baad isme built-in **Planner / Generator /
   Healer** agents aaye hain (MCP ke through).

3. **CI me AI:** flaky test detection, failure ka auto-analysis, aur
   AI-suggested fixes ab CI pipelines me aa rahe hain.

> Aapke roadmap ka Phase 5 (Ragas, DeepEval, promptfoo) isi family ka hai —
> lekin woh *LLM output* test karne ke liye. CI/CD pehle aata hai kyunki
> woh "plumbing" hai jisme yeh saare AI-eval tools chalte hain.

⚠️ Ek caution: AI-generated tests ko bina samjhe commit mat karna. CI tabhi
value deti hai jab tests *trustworthy* ho. AI draft de, decision aap lo.

---

## Part 5 — Aapke liye 2-week mini-plan

| Din | Kaam |
|-----|------|
| 1–2 | Yeh demo repo push karo, pipeline green karo, jaan-boojh kar todo/theek karo |
| 3–4 | Branch protection + 2-3 naye tests khud likho |
| 5–7 | Apne ek chhote product module ke unit tests CI me daalo |
| 8–10 | Playwright E2E ek job me add karo |
| 11–14 | Detection-accuracy gate ka prototype banao (F1 threshold) |

---

## Quick reference — commands
```bash
pytest -v                       # saare tests
pytest -v --cov=.               # coverage ke saath
ruff check .                    # lint
ruff check . --fix              # lint auto-fix
```

## Aage seekhne ke liye keywords (search/study)
`matrix builds` · `caching in CI` · `artifacts` · `secrets` ·
`environment protection rules` · `reusable workflows` · `concurrency groups` ·
`Docker build in CI` · `OIDC cloud auth` · `Playwright MCP`

---

*Yeh guide June 2026 ki current GitHub Actions + AI-testing practices par based hai.
Tools tezi se badalte hain — official GitHub Actions docs hamesha latest source rahega.*

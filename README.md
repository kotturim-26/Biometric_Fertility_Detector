# Biometric Fertility Detector

> ⚠️ **Proof of concept — not a medical device.** This project is a research prototype using simulated sensor data. It is not intended for clinical use or to replace medical advice.

A cycle-aware fertility tracking prototype that replaces the calendar method with real-time biometric signal processing. Built to address the **7.32-day mean absolute error (MAE)** in ovulation prediction for users with irregular cycles ([Meng et al., JMIR 2025](https://doi.org/10.2196/59550)), with a target reduction to **≤1.5-day MAE**.

<img width="795" height="408" alt="image" src="https://github.com/user-attachments/assets/88d32792-ad14-4985-921e-28a94a173f94" />


---

## The Problem

Most fertility tracking apps assume a 28-day cycle and apply a fixed calendar offset to predict ovulation. For the ~30% of users with irregular, long, or short cycles, this method breaks down — producing prediction errors as large as 7+ days during the critical fertile window.

The calendar method also ignores the physiological signals that actually govern ovulation timing.

---

## The Approach

This prototype combines two complementary biometric signals available from the **Oura Ring**:

| Signal | Why it matters |
|---|---|
| **Skin Temperature (BBT proxy)** | Rises ~0.2–0.5°F post-ovulation due to progesterone surge; nadir precedes ovulation |
| **Heart Rate Variability (HRV)** | Drops sharply around ovulation as sympathetic tone increases |

Using both signals together is more robust than either alone: temperature alone has a 1–2 day lag, while HRV captures the pre-ovulatory shift in real time.

### Architecture

```
Oura Ring biometrics (simulated)
        │
        ▼
Sliding-window signal processor
  • Detects BBT nadir + post-ovulatory rise
  • Detects HRV suppression window
  • Fuses both signals with cycle-length-adaptive weights
        │
        ▼
Ovulation day estimate + 6-day fertile window
        │
        ▼
LLM layer (natural language explanation)
  • Translates biometric patterns into plain-language insight
  • "Your HRV dropped 18% over the last 3 days, consistent
     with the pre-ovulatory LH surge..."
```

---

## Features

- **Cycle-length adaptive** — works for cycles of any length (21–45 days), not just 28-day assumptions
- **Dual-signal fusion** — BBT + HRV processed with a deterministic sliding-window detector
- **Interactive dashboard** — adjust cycle length and watch ovulation detection update in real time
- **Plain-language explanations** — integrated LLM translates biometric patterns into clinician-reviewed language
- **Fertile window visualization** — 6-day window highlighted with ovulation confidence indicator

---

## Tech Stack

```
Python 3.11+
├── Streamlit          — dashboard UI
├── Pandas / NumPy     — signal processing pipeline
├── Plotly             — dual-axis biometric visualization
└── Anthropic API      — natural language clinical explanations
```

---

## Run Locally

```bash
git clone https://github.com/maanasvi-kotturi/biometric-fertility-detector
cd biometric-fertility-detector

pip install -r requirements.txt

# Add your API key to .env
echo "ANTHROPIC_API_KEY=your_key_here" > .env

streamlit run app.py
```

---

## Publicly Deployed Web App Link
https://biometricfertilitydetector-egs79ogayhfvsomvn2vfe8.streamlit.app/

## Current Status & Roadmap

| Milestone | Status |
|---|---|
| Dual-signal sliding-window detector | ✅ Complete |
| Interactive Streamlit dashboard | ✅ Complete |
| LLM explanation layer | ✅ Complete |
| Validation against real Oura Ring export data | 🔲 Planned |
| MAE benchmarking vs. JMIR 2025 baseline | 🔲 Planned |
| Irregular cycle stress testing (cycle length 21–45d) | 🔲 Planned |

---

## Background & Motivation

Built as part of a broader interest in reproductive health technology. The signal processing approach draws on published literature linking HRV suppression to the pre-ovulatory LH surge and the well-documented biphasic BBT pattern described in fertility awareness literature.

---

## References

- Meng et al. (2025). *Accuracy of Menstrual Cycle Tracking Apps...* JMIR. https://doi.org/10.2196/59550
- Baker et al. (2001). *Quantification of the rise in basal body temperature at ovulation.* Fertility and Sterility.
- Gudmundsdottir et al. (2020). *Heart rate variability across the menstrual cycle.* Journal of Clinical Medicine.

---

## Author

**Maanasvi Kotturi** · BS Biomedical Engineering, UT Austin
[LinkedIn](https://www.linkedin.com/in/maanasvi-kotturi/) · [GitHub](https://github.com/maanasvi-kotturi)

# Image Classification Taxonomy & Guidelines (Label Studio)

This taxonomy supports research on **visual content posted by Instagram groups**. It is designed for **image classification** tasks in Label Studio and aims to capture **scene type**, **stance**, **potential support for terrorism**, and **emotional impact**. The focus is descriptive and analytical; **annotators must not add or promote harmful content**.

> **Important ethics note:** Annotate neutrally and descriptively. If content appears to advocate violence, record it without amplifying or sharing it beyond the research workflow. Follow platform and institutional guidelines for handling extremist imagery.

---

## Fields

### 1) Emotional content (single choice, required)
- **Yes (clearly emotional):** The image is crafted to elicit strong feelings (e.g., grief, outrage, fear, pride).  
- **No (neutral/informational):** Mostly descriptive (e.g., infographic, map, plain event notice).  
- **Unclear:** Insufficient evidence.

### 2) Text present (single choice, required)
- **Text visible:** Any readable text in the image (banners, captions, posters).
- **No text.**

> If text is present, transcribe the **key parts** in _Visible Text_ (Section 6). You can be brief; capture phrases that drive meaning (e.g., “Boycott X”, “Free Y”).

### 3) Scene types (multi-select)
Select all that apply:
- **War zone / active conflict** — explosions, rubble, armed units in action.
- **Children present** — minors clearly shown.
- **Encampment / camp** — tents, temporary shelters, refugee/IDP settings.
- **Call for demonstration / protest announcement** — flyer-style, date+place.
- **Solidarity campaign / awareness** — ribbons, frames, slogans of support.
- **Call for boycott / divestment / sanctions (BDS).**
- **Interview / talk show / speaker portrait** — studio-style, lower-thirds, headshots.
- **Military / army / police presence.**
- **Protest / rally in progress.**
- **Vandalism / property damage.**
- **Political leader / spokesperson featured.**
- **Religious site / ritual / event.**
- **Flag / symbol prominently displayed.**
- **Fundraising / donation ask.**
- **Memorial / vigil / candles.**
- **Graphic violence (non-gore).**
- **Graphic violence (gore).**
- **Other / not listed** — add details in **Notes**.

### 4) Does the image contain **support for a terrorist organization**? (single, required)
- **Yes** — explicit praise, propaganda, recruitment, or endorsement signals (e.g., logos, pledges, slogans) that **clearly** support a designated terrorist organization.
- **No** — none of the above.
- **Ambiguous / Unclear** — signals are indirect, coded, or context is missing.

> When selecting **Yes**, briefly note **which organization** and the **evidence** (e.g., specific insignia, slogans) in **Notes**. If unsure, choose **Ambiguous / Unclear** and record what you see.

### 5) Stance or target (multi-select, optional)
- **Pro-Israel**
- **Anti-Israel**
- **Pro-Palestinian**
- **Anti-Zionist**
- **Anti-Jewish (antisemitic content)** — e.g., slurs, stereotypes, Holocaust trivialization.
- **Pro-specific organization (named)**
- **Other / N/A**

> Use this field to capture **stance** and **target** when present; avoid inferring beyond the visible content.

### 6) Emotional impact (rating + dominant emotion)
- **Rating (1–7):** Your **subjective** estimate of how strongly the image is likely to affect a **general audience** (1 = not emotional, 7 = extremely emotional). Consider salience, imagery intensity, cues like crying, injuries, or patriotic display, and persuasive design.
- **Dominant emotion (single choice):** The main emotion the image appears to evoke: **Anger, Fear, Sadness, Disgust, Joy, Pride, Empathy/Compassion, Guilt/Shame, Awe, Neutral, Other**.

### 7) Visible text (free text)
Transcribe key words/phrases that shape meaning. Don’t worry about perfect OCR; focus on **salient** text (chants, demands, organization names).

### 8) Notes (free text)
State the **minimal rationale** for key decisions and list any **symbols/logos/flags** used as evidence.

---

## Suggested Annotation Rules

1. **Be literal:** Label what is **visible**; avoid political inference.  
2. **Err on “Ambiguous/Unclear”** when evidence is thin.  
3. **Use Notes** to capture short justifications (e.g., “green emblem with crossed swords on banner”).  
4. **Respect safety:** If imagery is graphic, tag the appropriate **Graphic violence** option.  
5. **Consistency matters:** Revisit a few labeled items together weekly to keep interpretation aligned.

---

## Optional Extensions (easy to add later)

- **Actors (multi):** civilians, activists, militants, police, politicians, journalists, children.  
- **Symbols (multi):** specific flags, emblems; create a controlled list as you discover frequent ones.  
- **Call-to-action (multi):** donate, attend, share, boycott, subscribe, recruit.  
- **Media type (single):** photo, poster, meme, screenshot, infographic.  
- **Source platform (single):** Instagram, Facebook, X, Telegram, other.  

If you want these, I can extend the XML and taxonomy with controlled vocabularies.

---

## How to Use

1. Create a **new project** in Label Studio → **Settings → Labeling Interface → Code**.  
2. Paste the contents of `label_config.xml` into the editor and **Save**.  
3. Import your images; begin labeling.  
4. Export results as JSON (includes chosen fields).

---

## Versioning

- **v1.0 (initial)** — base categories + emotional impact rating.
- Keep changes backward compatible (append new multi-select options; avoid renaming fields).


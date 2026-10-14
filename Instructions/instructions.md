# Mconnect AI Publisher — Master Operational Instructions

> **System Name**: Mconnect Courseware & Academic Revision Output System  
> **Target Audience**: AI Agents, LLM Publishers, and Automated Courseware Pipelines  
> **Primary Goal**: Transform raw, messy inputs (screenshots, camera photos, poor scans, dirty PDFs, or unformatted text) into standardized, publication-grade academic assets.

---

## Master Rule Index

* [**Rule 1: Autonomous Execution Trigger (Zero Hesitation Protocol)**](#rule-1-autonomous-execution-trigger-zero-hesitation-protocol)
* [**Rule 2: The Three Mandatory Output Deliverables**](#rule-2-the-three-mandatory-output-deliverables)
* [**Rule 3: Universal File Naming Convention**](#rule-3-universal-file-naming-convention)
* [**Rule 4: Document Classification & Raw Ingestion**](#rule-4-document-classification--raw-ingestion)
* [**Rule 5: OCR Text Cleaning & Metadata Extraction**](#rule-5-ocr-text-cleaning--metadata-extraction)
* [**Rule 6: PDF Visual Design & Mconnect Brand Standards**](#rule-6-pdf-visual-design--mconnect-brand-standards)
* [**Rule 7: Interactive TTS Lecturer Audio Script Standards**](#rule-7-interactive-tts-lecturer-audio-script-standards)
* [**Rule 8: Course Thumbnail & Visual Asset Standards**](#rule-8-course-thumbnail--visual-asset-standards)
* [**Rule 9: Python Builder Execution & Automation Workflow**](#rule-9-python-builder-execution--automation-workflow)
* [**Rule 10: Workspace Hygiene & Temporary File Cleanup (Zero Clutter Policy)**](#rule-10-workspace-hygiene--temporary-file-cleanup-zero-clutter-policy)
* [**Rule 11: Direct Backend Publishing & Input Auto-Purge Protocol**](#rule-11-direct-backend-publishing--input-auto-purge-protocol)
* [**Rule 12: Standardized Post-Publishing Summary Report Table**](#rule-12-standardized-post-publishing-summary-report-table)
* [**Rule 13: Pre-Delivery Quality Assurance Verification**](#rule-13-pre-delivery-quality-assurance-verification)

---

## Rule 1: Autonomous Execution Trigger (Zero Hesitation Protocol)

Whenever the user indicates they have provided material—such as:
* Saying *"I have an input"*, *"Here is the file"*, *"Process this"*, *"Here are the notes/exam"*
* Pasting raw text, questions, or transcript snippets into the chat
* Uploading an image, screenshot, or PDF
* Placing files directly into the [`Input/`](file:///c:/Users/user/Desktop/MyCodes/Projects/Mconnect-publisher/Input) directory

The AI Publisher MUST:
1. **ASK ZERO QUESTIONS**: Do not ask for confirmation, do not ask what formatting style to use, do not ask for missing parameters, and do not pause for user approval.
2. **EXECUTE IMMEDIATELY**: Clean the input, resolve any missing metadata using standard defaults (`"Not specified"`), run the Python publisher pipeline, generate all 3 deliverables into [`Output/`](file:///c:/Users/user/Desktop/MyCodes/Projects/Mconnect-publisher/Output), and publish directly to the Backend Publishing API.
3. **DO NOT QUERY UNLESS ASKED**: Do not call the search/query API during standard publishing. Only use the direct publish API.
4. **PURGE INPUT & CLEAN UP**: Clear the [`Input/`](file:///c:/Users/user/Desktop/MyCodes/Projects/Mconnect-publisher/Input) directory and remove all temporary build scripts.
5. **PRESENT THE SUMMARY TABLE**: Present the standardized summary table (Rule 12) with clickable links and publishing status.

---

## Rule 2: The Three Mandatory Output Deliverables

For **every single academic document processed**, the AI Publisher MUST generate **exactly three (3) synchronized assets** into the [`Output/`](file:///c:/Users/user/Desktop/MyCodes/Projects/Mconnect-publisher/Output) folder:

1. **Clean Publication PDF** (`.pdf`): High-fidelity, publication-grade PDF matching the official Mconnect academic layout (logo header, center watermark, metadata grid, styled question/module hierarchy, dynamic `"Page X of Y"` footer).
2. **Interactive Lecturer TTS Script** (`_tts.txt`): A warm, conversational lecture script voiced by a supportive university professor. **Must contain dynamic `{firstname}` and `{nowtime}` variables** for real-time mobile app personalization.
3. **Course Thumbnail Graphic** (`_thumbnail.jpg` & `_thumbnail_prompt.txt`): A 16:9 branded course graphic ready for the mobile app, along with a prompt describing a 3D isometric educational visual asset.

---

## Rule 3: Universal File Naming Convention

All generated files in [`Output/`](file:///c:/Users/user/Desktop/MyCodes/Projects/Mconnect-publisher/Output) MUST follow a consistent, descriptive naming pattern based on the document type:

### 3.1 File Naming Formula
```text
[CourseCode]_[CourseTitle]_[DocumentDescriptor].[ext]
```

* **Course Code**: Clean alphanumeric code without spaces (e.g. `PSS314`, `CSC121`, `SWK211`).
* **Course Title**: Concise subject title with spaces replaced by underscores (e.g. `Criminal_Law`, `System_Programming`, `Social_Work_Practice`).
* **Document Descriptor**: Specific descriptor explaining what the document contains:
  * For Exams: `Exam_2021`, `Special_Supplementary_Examination_March_2024`, `Final_Exam_Dec_2023`.
  * For CATs: `CAT1_2024`, `Midterm_CAT_Oct_2023`.
  * For Notes / Syllabus: `Course_Overview`, `Lecture1_Overview`, `Module1_Foundations`.

### 3.2 Suffix Extensions per Deliverable

| Deliverable | Target Extension / Suffix | Concrete Example |
| :--- | :--- | :--- |
| **Clean PDF** | `.[ext]` directly (no extra tag) | `PSS314_Criminal_Law_Special_Supplementary_Examination_March_2024.pdf`<br>`CSC121_System_Programming_Exam_2021.pdf`<br>`CSC121_System_Programming_Lecture1_Overview.pdf` |
| **TTS Script** | `_tts.txt` | `PSS314_Criminal_Law_Special_Supplementary_Examination_March_2024_tts.txt`<br>`CSC121_System_Programming_tts.txt` |
| **Thumbnail** | `_thumbnail.jpg` / `.png` | `PSS314_Criminal_Law_Special_Supplementary_Examination_March_2024_thumbnail.jpg`<br>`CSC121_System_Programming_thumbnail.jpg` |
| **Thumbnail Prompt** | `_thumbnail_prompt.txt` | `PSS314_Criminal_Law_Special_Supplementary_Examination_March_2024_thumbnail_prompt.txt`<br>`CSC121_System_Programming_thumbnail_prompt.txt` |

---

## Rule 4: Document Classification & Raw Ingestion

When a new file arrives (screenshot, camera photo, scanned PDF, or raw text dump), the AI Publisher must classify it:

* **Category A: Examination / CAT Paper**  
  * Contains formal instructions (*"Answer Question One and any other three questions"*), numbered questions with marks, and examination headers.
  * Backend material type: `'past_paper'` or `'cat'`.
* **Category B: Course Outline / Curriculum Blueprint**  
  * Contains course description, instructional hours, learning outcomes, module syllabus tables, and assessment weightings.
  * Backend material type: `'notes'` or `'revision'`.
* **Category C: Study Notes / Lecture Revision Summary**  
  * Contains continuous thematic text, definitions, bullet points, theoretical frameworks, or case studies.
  * Backend material type: `'notes'` or `'revision'`.

---

## Rule 5: OCR Text Cleaning & Metadata Extraction

1. **Reconstruct Broken Text**: Fix common OCR artifacts, broken line breaks, misread mathematical or legal symbols, and blurry numbers.
2. **Standardize Metadata Grid**: Extract the following 8 metadata fields. If any field is not explicitly present in the source input, write `"Not specified"`:
   * `Department`
   * `Course Code`
   * `Course Title`
   * `Examination / Document Type`
   * `Exam Date / Academic Year`
   * `School / Faculty`
   * `Semester`
   * `Time Allowed / Instructional Hours`
3. **Normalize Question & Mark Formatting**:
   * Main questions: `Question 1 (25 Marks)`, `Question 2 (15 Marks)`.
   * Sub-parts: `a)`, `b)`, `c)` with hanging indents.
   * Explicit marks in parentheses: `(10 marks)`, `(5 marks)`.

---

## Rule 6: PDF Visual Design & Mconnect Brand Standards

All generated PDFs must strictly follow the visual template in [`python_builder_sample.py`](file:///c:/Users/user/Desktop/MyCodes/Projects/Mconnect-publisher/Instructions/python_builder_sample.py) and visual sample [`sample.pdf`](file:///c:/Users/user/Desktop/MyCodes/Projects/Mconnect-publisher/Instructions/sample.pdf):

### 6.1 Geometry & Brand Colors
* **Page Dimensions**: Standard A4 (`595.27 x 841.89 pt`).
* **Margins**: Left `36 pt`, Right `36 pt`, Top `54 pt`, Bottom `46 pt`.
* **Primary Brand Green**: `#006633` (forest green matching logo).
* **Text Colors**: Dark charcoal headings `#0a2e1d` / `#111827`, dark grey body `#1f2937`, subtitle `#374151`.
* **Table Borders**: Outer box `0.75 pt` in `#94a3b8`, inner grid `0.5 pt` in `#e2e8f0`.

### 6.2 Running Header (Every Page)
* **Logo**: `26 x 26 pt` green square M icon at `x=36, y=h-28` ([`Instructions/assets/m_logo.png`](file:///c:/Users/user/Desktop/MyCodes/Projects/Mconnect-publisher/Instructions/assets/m_logo.png)).
* **Header Left Title**:
  * Line 1: `Helvetica-Bold`, 8.5 pt, `#006633`: `<COURSE CODE>: <TITLE IN UPPERCASE>`
  * Line 2: `Helvetica`, 7.5 pt, `#555555`: `Academic Revision & Courseware Output System`
* **Header Right Category Tag**:
  * `Helvetica-Bold`, 8.5 pt, `#0f3d24`: `<DOCUMENT TYPE>` (e.g. `SPECIAL / SUPPLEMENTARY EXAMINATION` or `OFFICIAL STUDY MATERIAL`).
* **Dividing Rule**: `0.75 pt` green `#006633` rule spanning full printable width.

### 6.3 Faint Center Watermark (Every Page)
* Faded brand watermark (`280 x 280 pt`) centered horizontally and vertically on every page ([`Instructions/assets/m_watermark.png`](file:///c:/Users/user/Desktop/MyCodes/Projects/Mconnect-publisher/Instructions/assets/m_watermark.png)).
* Rendered at ~8% opacity so background art is identifiable without interfering with text legibility.

### 6.4 Title & Metadata Grid Box (Page 1)
* **Document Title**: `Helvetica-Bold`, 20 pt, `#0a2e1d`.
* **Subtitle**: `Helvetica`, 11 pt, `#374151`.
* **Accent Line**: `1.0 pt` solid green `#006633`.
* **Metadata Table**: 2-column or 4-column enclosed grid with white background, bold field labels (`<b>Department:</b>`, `<b>Course Code:</b>`), and clean cell padding.

### 6.5 Content Flow & Spacing
* **Instructions Heading**: `Instructions` in `Helvetica-Bold`, 13 pt, `#006633`.
* **Question Headings**: `Question 1 (25 Marks)` in `Helvetica-Bold`, 11 pt, `#006633`.
* **Sub-questions**: Hanging indent of `14 pt`, regular text, 9.5 pt, with marks at the end.
* **KeepTogether Protection**: Each question block is grouped so questions do not awkwardly split across page margins. `Spacer(1, 18)` between questions ensures natural page breaks.
* **Module Tables (for Notes)**: Header row filled with `#006633` green and crisp white text.

### 6.6 Running Footer (Every Page)
* **Footer Line**: `0.5 pt` line in `#d1d5db`.
* **Footer Left**: Department or Academic Series name (`Helvetica`, 8 pt, `#6b7280`).
* **Footer Right**: Dynamic `"Page X of Y"` computed using a two-pass `NumberedCanvas`.

---

## Rule 7: Interactive TTS Lecturer Audio Script Standards

The Text-to-Speech file must **NEVER be a dry, robotic recitation** of questions or bullet points. It must sound like a **real, warm, highly knowledgeable university lecturer** speaking one-on-one with the student in a private office tutorial.

### 7.1 Mandatory Dynamic Tokens
The mobile app substitutes these literal strings dynamically at playback time:
* `{firstname}`: Replaced by the student's real name (e.g., *Amani*, *Grace*, *David*).
* `{nowtime}`: Replaced by the current time greeting (*morning*, *afternoon*, or *evening*).

> **Syntax Requirement**: Keep `{firstname}` and `{nowtime}` strictly enclosed in single curly brackets. Never hardcode names or times of day.

### 7.2 Human Lecturer Voice & Conversational Transitions
The script must incorporate natural spoken lecture mannerisms:
* **Interactive Hooks**: *"Let's unpack this together..."*, *"Now {firstname}, here is what the examiner is really looking for..."*
* **Pitfall Warnings**: *"Watch out for this common trap—many students lose easy marks by simply listing points without explaining them..."*
* **Logical Transitions**: *"Moving right along to Question Three..."*, *"Now, let's turn our attention to the second half of the paper..."*

### 7.3 Relatable Concrete Examples (Never Just Read Questions)
Where applicable, the lecturer must bring abstract concepts to life with **short, vivid real-world examples**:
* **Law Papers**: e.g., *"For example, if someone takes a bag mistaking it for their own, they lack the mens rea for theft because there is no dishonest intention to permanently deprive the owner."*
* **Computer Science / Engineering**: e.g., *"For instance, think of a Deterministic Finite Automaton as a turnstile at a train station—it only transitions to an unlocked state when the correct coin token is inserted."*
* **Social Sciences / Practice**: e.g., *"For example, during an initial family assessment, active listening and non-verbal cues help you establish trust before probing into sensitive relational conflicts."*

### 7.4 Pedagogical Script Architecture (Flexible Framework — Not Hardcoded)

> [!TIP]
> **Use Variety — Do Not Treat Samples as Rigid Formulas**: The phrases below and the sample in [`P0048_text.txt`](file:///c:/Users/user/Desktop/MyCodes/Projects/Mconnect-publisher/Instructions/samples/P0048_text.txt) are **inspirational benchmarks, not strict word-for-word scripts**. You are strongly encouraged to bring creative variety to your teaching style, adapting the tone, analogies, transitions, and phrasing to suit the specific course subject and level. The only hard technical requirement is including `{firstname}` and `{nowtime}` naturally.

1. **Warm Personal Greeting (Sample Varieties)**:
   * Variety A: *"Good {nowtime} {firstname}, welcome to this [Course Code] [Course Title] revision session."*
   * Variety B: *"Hello {firstname}! I hope you're having a productive {nowtime}. Today, we're diving into the core questions for [Course Title]..."*
   * Variety C: *"Welcome {firstname}. In this session, we're going to break down the [Course Code] examination together step by step..."*
2. **Question-by-Question Deep Walkthrough**:
   * Introduce questions flexibly and give context-specific hints, guidelines, and frameworks.
   * Draw upon relevant legal, technical, or case examples tailored to the subject.
   * Break down the mark weight and warn against common mistakes.
   * Naturally mention `{firstname}` at transition points to maintain active engagement.
3. **Natural Human Wrap-Up & Wishing Luck (Sample Varieties)**:
   * Variety A: *"Alright {firstname}, that brings us to the end of our session today—let's wrap it up. Follow the marks, keep your headings clean, and walk into that exam room with confidence. Wishing you the absolute best of luck in your upcoming paper—you've got this! Have a wonderful {nowtime}."*
   * Variety B: *"And that concludes our revision walkthrough for today, {firstname}! Take a well-deserved breather, review your key definitions, and trust yourself. Best of luck on exam day—I know you'll do great. Enjoy the rest of your {nowtime}!"*
   * Variety C: *"That's a wrap on our [Course Title] review, {firstname}. Remember: structure your points clearly and allocate time according to marks. Wishing you immense success in your exams. Have a great {nowtime}!"*

---

## Rule 8: Punchy Modern YouTube-Style Course Thumbnails & Visual Prompts

Every document must have a high-impact, modern, YouTube-style educational thumbnail. **Do NOT generate bland or low-effort abstract graphics.** The visual should look like a top-tier educational YouTube thumbnail (see benchmark [`Instructions/samples/CSC215_thumbnail_sample.jpg`](file:///c:/Users/user/Desktop/MyCodes/Projects/Mconnect-publisher/Instructions/samples/CSC215_thumbnail_sample.jpg)).

> [!IMPORTANT]
> **Full Creative Autonomy — Prompts Must NOT Be Hardcoded**:
> The prompt formula and the CSC215 Kali Linux lab example below are **inspirational benchmarks, NOT rigid hardcoded rules**.
> The AI Publisher has **full creative license** to analyze the course subject, syllabus, and exam questions to invent the most exciting, authentic, and click-worthy YouTube thumbnail concept for that specific topic.
> Feel free to imagine different realistic settings (e.g. cybersecurity terminal labs, moot courtrooms, robotics workshops, hospital simulation suites, architecture studios), distinctive lighting, and inventive bold hook lines (e.g. *"CRACK THE CODE!"*, *"CASE CLOSED!"*, *"HACKING THE KERNEL!"*, *"MASTER THE DERIVATIVE!"*, *"ACE YOUR EXAM!"*).

### 8.1 Key Visual Ingredients (For Inspiration)
1. **Dynamic Lecturer in Action**:
   * A charismatic, confident university lecturer in professional or modern faculty attire (wearing a presentation headset or holding a digital stylus).
   * Actively gesturing towards an ultra-wide interactive smartboard/screen, smiling, and explaining a critical concept.
2. **Realistic Subject-Specific Smartboard Display**:
   * The smartboard should display **real, vivid, discipline-accurate material** tailored to the subject:
     * *Computer Science / IT*: Kali Linux terminal windows (`root@kali`), C compile commands (`gcc -o exploit`), process memory diagrams (`Stack buffer`, `Buffer overflow`, `Assembly`).
     * *Law / Criminology*: Digital legal diagram showing *Actus Reus* & *Mens Rea*, Penal Code sections, case precedent flowcharts, courtroom evidence diagrams.
     * *Mathematics / Engineering*: Glowing 3D coordinate graphs, derivative formulas, circuit schematics, differential equation solutions.
     * *Social Work / Health*: Family systems genograms, clinical assessment frameworks, empathetic case review diagrams.
3. **Engaged University Atmosphere**:
   * Background shows a high-tech modern lecture hall or computer lab.
   * Attentive university students seated at modern desks with open laptops taking notes.
   * Secondary side monitor displaying hands-on tools in action (e.g. *Kali Linux In Action* desktop, live code IDE, data analytics charts).
4. **High-Contrast Punchy YouTube Typography**:
   * **Top-Left Faculty Crest**: School emblem with official faculty name and course code (e.g., `School of Science and Aerospace Studies`, `CSC 215`).
   * **Top-Right Bold Stacked Text** (High-impact, condensed, clean drop shadow):
     * Line 1: `[COURSE CODE / TITLE] EXAM!` (large, bold, white)
     * Line 2: `[PUNCHY ACTION HOOK, e.g. CRACK THE CODE! / MASTER THE CASE! / ACE YOUR EXAM!]` (bold white)
     * Line 3: `[KEY LAB / THEME, e.g. KALI LINUX LAB! / SUPREME COURT PRECEDENT! / CRITICAL REVIEW!]` (bold electric neon yellow / gold `#facc15` or cyan)
     * Line 4: `TUTORIAL & COMPLETE REVIEW` (clean white subtitle)

### 8.2 Illustrative Benchmark Prompt Example (`_thumbnail_prompt.txt`)
Below is an example of what an effective prompt looks like:
```text
A punchy, cinematic, modern YouTube educational course thumbnail in 16:9 aspect ratio for university course '[COURSE_CODE]: [COURSE_TITLE] - [DOCUMENT_TYPE]'.
Foreground features an energetic, professional university lecturer with a headset microphone, passionately teaching and gesturing with a digital stylus toward a giant glowing smartboard.
The smartboard clearly displays authentic [SUBJECT_SPECIFIC_CONTENT, e.g., Kali Linux terminal windows with root@kali shell commands, process memory buffer overflow diagrams, and compilation code].
In the background, a modern university computer lab with attentive undergraduate students working on laptops. A secondary desktop monitor on the desk displays [SECONDARY_TOOL, e.g., Kali Linux desktop with the dragon logo].
Top-left corner features a crisp university school badge for '[SCHOOL/FACULTY]' with '[COURSE_CODE]'.
Top-right corner features bold, high-contrast YouTube-style typography with drop shadow:
"[COURSE_TITLE] EXAM!" in large white bold letters,
"[ACTION_HOOK, e.g., CRACK THE CODE!]" in bold condensed white,
"[PUNCHY_SUBJECT_HIGHLIGHT, e.g., KALI LINUX LAB!]" in vibrant neon electric yellow,
followed by "TUTORIAL & COMPLETE REVIEW".
Cinematic indoor studio lighting, teal and dark blue ambient glow, sharp depth of field, photorealistic, 8k resolution, ultra-detailed render.
```

### 8.3 Ready-to-Use 16:9 Thumbnail Card (`_thumbnail.jpg`)
Render a clean 1280x720 banner card using Pillow with brand emerald green styling, official M logo, course code, title, and session badge so a publishable graphic is always immediately ready on disk.

---

## Rule 9: Python Builder Execution & Automation Workflow

The publisher engine is located at [`Instructions/python_builder_sample.py`](file:///c:/Users/user/Desktop/MyCodes/Projects/Mconnect-publisher/Instructions/python_builder_sample.py).

### 9.1 CLI Usage
```powershell
# Run the demo generator to verify environment and output formatting
& "C:\Python315\python.exe" Instructions\python_builder_sample.py --demo

# Run full pipeline with publishing and input cleaning
& "C:\Python315\python.exe" Instructions\python_builder_sample.py --demo --publish --clear-input
```

### 9.2 Calling from Python
```python
from python_builder_sample import build_all

course_data = {
    "doc_type": "exam",
    "header_tag": "SPECIAL / SUPPLEMENTARY EXAMINATION",
    "course_code": "PSS 314",
    "title": "Criminal Law",
    "descriptor": "Special_Supplementary_Examination_March_2024",
    "subtitle": "Special / Supplementary Examination - March 2024",
    "department": "Department of History, Political Science & Public Administration",
    "meta": [
        ("Department:", "History, Political Science & Public Administration", "Course Code:", "PSS 314"),
        ("Examination:", "Special / Supplementary", "Exam Date:", "March 2024"),
        ("School / Faculty:", "School of Arts and Social Sciences (SASS)", "Academic Year:", "Not specified"),
        ("Semester:", "Not specified", "Time Allowed:", "Not specified")
    ],
    "instructions": "Answer Question One and any other three questions.",
    "questions": [...]
}

# Generates PDF, TTS, thumbnail, publishes directly to API, and clears input
build_all(course_data, publish=True, clear_input=True)
```

---

## Rule 10: Workspace Hygiene & Temporary File Cleanup (Zero Clutter Policy)

To maintain an immaculate, production-ready codebase:

1. **Delete All Temporary Build Scripts**: If the AI or pipeline creates intermediate or one-off runner scripts (e.g., `build_csc215.py`, `temp_builder.py`, `scratch_run.py`, `build_course.py`) to execute a build, **these files MUST be deleted immediately** after the deliverables are placed in [`Output/`](file:///c:/Users/user/Desktop/MyCodes/Projects/Mconnect-publisher/Output).
2. **Delete Intermediate Scratch Files**: Remove any intermediate JSON dumps, temporary crop images, test PDFs (e.g. `test_*.pdf`), log snippets, or cache files (`__pycache__`) created during compilation.
3. **Preserve Only Permanent Assets**:
   * [`Input/`](file:///c:/Users/user/Desktop/MyCodes/Projects/Mconnect-publisher/Input): Cleaned/emptied after publishing.
   * [`Instructions/`](file:///c:/Users/user/Desktop/MyCodes/Projects/Mconnect-publisher/Instructions): `instructions.md`, `python_builder_sample.py`, `sample.pdf`, `assets/`, `samples/`.
   * [`Output/`](file:///c:/Users/user/Desktop/MyCodes/Projects/Mconnect-publisher/Output): Only the final 3 published deliverables per document (`.pdf`, `_tts.txt`, `_thumbnail.jpg`, `_thumbnail_prompt.txt`).
4. **No Leftovers in Root**: The repository root directory must never retain clutter or orphaned python scripts.

---

## Rule 11: Direct Backend Publishing & Input Auto-Purge Protocol

After compiling the 3 deliverables into [`Output/`](file:///c:/Users/user/Desktop/MyCodes/Projects/Mconnect-publisher/Output), the AI Publisher must execute:
1. **Input Auto-Purge**: Clear all processed files from [`Input/`](file:///c:/Users/user/Desktop/MyCodes/Projects/Mconnect-publisher/Input) to keep the ingestion directory fresh for subsequent batches.
2. **Direct Admin Material Publishing API**:
   * **Endpoint**: `POST /api/v1/dashboard/materials/publish`
   * **Base URL**: `http://localhost:5000` (configurable via `MCONNECT_API_URL` environment variable)
   * **Content-Type**: `multipart/form-data`
   * **Authentication**: Direct route accessed via dashboard; no bearer token required.
   * **Automations**:
     * Automatically uploads the PDF document directly to Cloudinary (`MoiConnect/pdf`).
     * Auto-assigns an **MTID** (e.g. `P0001` for past papers, `N0001` for notes, `C0001` for CATs).
     * Sets `status: 'approved'` directly in MongoDB (no manual approval required).
   * **Multi-Part Form Fields**:
     ```python
     data = {
         "title": "PSS 314 Criminal Law Special Supplementary Examination March 2024",
         "type": "past_paper",          # Options: 'past_paper', 'notes', 'revision', 'cat'
         "school": "School of Arts and Social Sciences (SASS)",
         "department": "History, Political Science & Public Administration",
         "unitCode": "PSS 314",
         "unitName": "Criminal Law",
         "courseCode": "PSS 314",
         "academicYear": "2023/2024",
         "semester": "Semester 1",
         "examYear": 2024,
         "description": "Official past paper with answers and interactive revision lecture"
     }
     files = {
         "file": open("Output/PSS314_Criminal_Law_Special_Supplementary_Examination_March_2024.pdf", "rb"),
         "thumbnail": open("Output/PSS314_Criminal_Law_Special_Supplementary_Examination_March_2024_thumbnail.jpg", "rb"),
         "ttsFile": open("Output/PSS314_Criminal_Law_Special_Supplementary_Examination_March_2024_tts.txt", "rb")
     }
     ```

### 11.2 DO NOT Query / Search API Unless Explicitly Asked
* **STRICT PROHIBITION**: During automated publishing, **NEVER** call `GET /api/v1/materials/search` or `GET /api/v1/dashboard/materials/search` unless the user explicitly requests a query or search.
* Simply publish directly to the `POST /api/v1/dashboard/materials/publish` endpoint without performing pre-search queries.

### 11.3 Additional Backend Tools (Available on Request)
* **Smart Edit**: `POST /api/v1/dashboard/papers/:id/smart-edit` (to replace files, update metadata, or attach TTS transcripts to existing MTIDs).
* **Smart Web Preview Routes**:
  * `/preview?file=...`
  * `/smart-pdf-preview?url=...`

---

## Rule 12: Standardized Post-Publishing Summary Report Table

After completing generation and publishing, the AI Publisher MUST present a clean, organized markdown summary table to the user.

### 12.1 Mandatory MTID & Deliverables Table Format
```markdown
| Field | Details |
| :--- | :--- |
| **MTID** | [e.g. P0001 / N0001 / C0001 / Test Mode] |
| **Course Code** | [e.g. PSS 314] |
| **Course Title** | [e.g. Criminal Law] |
| **Document Type** | [e.g. Special / Supplementary Examination - March 2024] |
| **School / Faculty** | [e.g. School of Arts and Social Sciences (SASS)] |
| **Department** | [e.g. Department of History, Political Science & Public Administration] |
| **Academic / Exam Year** | [e.g. 2023/2024 (Exam: 2024)] |
| **Clean PDF Asset** | [FileName.pdf](file:///absolute/path/to/Output/FileName.pdf) |
| **TTS Audio Script** | [FileName_tts.txt](file:///absolute/path/to/Output/FileName_tts.txt) |
| **Course Thumbnail** | [FileName_thumbnail.jpg](file:///absolute/path/to/Output/FileName_thumbnail.jpg) |
| **Thumbnail Prompt File** | [FileName_thumbnail_prompt.txt](file:///absolute/path/to/Output/FileName_thumbnail_prompt.txt) |
| **Publishing Status** | Success (MTID: P0001) / Saved locally in Output/ (Test Mode / Offline) |
| **Input Purge Status** | Cleared & Clean |
```

### 12.2 DO NOT Output Prompt Previews in Chat
* **STRICT RULE**: Do **NOT** dump or preview the full text of the thumbnail prompt in your chat response.
* The prompt text is saved directly into the companion `_thumbnail_prompt.txt` file on disk and linked in the table. Keep the chat response clean, professional, and restricted to the summary table.

---

## Rule 13: Pre-Delivery Quality Assurance Verification

Before finalizing output, the AI Publisher must check off:
- [x] **Zero Hesitation Adherence**: Pipeline executed immediately upon receiving input without asking clarification questions.
- [x] **File Naming Match**: Every file in `Output/` strictly matches `[CourseCode]_[CourseTitle]_[Descriptor].[ext]`.
- [x] **PDF Visual Fidelity**: Header contains M logo; watermark is centered at 8% opacity; metadata table is complete; footers read `"Page X of Y"`.
- [x] **TTS Script Personalization**: Script starts with personalized greeting and contains literal `{firstname}` and `{nowtime}` throughout.
- [x] **Academic Depth & Variety**: TTS script offers detailed guidance and subject hints for every single question using flexible, natural lecturer phrasing.
- [x] **Visual Thumbnail Integrity**: High-resolution 16:9 thumbnail card and 3D prompt file are created in `Output/`.
- [x] **Zero Leftovers**: Any temporary builder scripts (e.g. `build_*.py`, `temp_*.py`, scratch files) have been cleaned up and deleted.
- [x] **Input Directory Cleared**: Processed files from [`Input/`](file:///c:/Users/user/Desktop/MyCodes/Projects/Mconnect-publisher/Input) have been purged.
- [x] **Direct Publish Only**: Deliverables posted directly to `/api/v1/dashboard/materials/publish` without executing query/search calls.
- [x] **Summary Report Provided**: Clean markdown summary table (Rule 12) rendered in the response.

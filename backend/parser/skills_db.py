"""
Database skill keywords (rule-based).
Disusun untuk konteks rekrutmen startup Indonesia (lihat 2.3 PDF).

Struktur kamus dipisah per kategori agar mudah dikembangkan minggu ke-2
ketika modul AI Scoring memerlukan bobot per-kategori.
"""

TECHNICAL_SKILLS = {
    # Programming languages
    "Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#", "Go",
    "Ruby", "PHP", "Kotlin", "Swift", "Rust", "Scala", "R", "Dart",

    # Web / mobile frameworks
    "React", "Vue", "Vue.js", "Angular", "Next.js", "Nuxt", "Svelte",
    "Node.js", "Express", "Django", "Flask", "FastAPI", "Laravel",
    "Spring", "Spring Boot", "Flutter", "React Native",

    # Database
    "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite", "Oracle",
    "SQL Server", "Firebase", "DynamoDB", "Elasticsearch", "SQL",

    # Data / AI
    "Machine Learning", "Deep Learning", "Data Analysis", "Data Science",
    "TensorFlow", "PyTorch", "Keras", "scikit-learn", "Pandas", "NumPy",
    "NLP", "Computer Vision", "spaCy", "OpenCV",

    # DevOps & Tools
    "Git", "GitHub", "GitLab", "Docker", "Kubernetes", "Linux", "Bash",
    "Jenkins", "AWS", "GCP", "Azure", "Terraform", "Ansible", "CI/CD",

    # Office / produktivitas
    "Microsoft Excel", "Microsoft Word", "Microsoft PowerPoint",
    "Google Sheets", "Google Docs", "Tableau", "Power BI", "Looker",

    # Desain
    "Figma", "Adobe Photoshop", "Adobe Illustrator", "Canva",
    "Adobe XD", "Sketch", "CorelDraw",
}

SOFT_SKILLS = {
    "Komunikasi", "Communication", "Leadership", "Kepemimpinan",
    "Teamwork", "Kerja Sama Tim", "Problem Solving", "Analytical Thinking",
    "Time Management", "Manajemen Waktu", "Adaptability", "Adaptasi",
    "Public Speaking", "Negotiation", "Critical Thinking",
}

ALL_SKILLS: set[str] = TECHNICAL_SKILLS | SOFT_SKILLS

# Lookup case-insensitive (lower -> bentuk kanonik)
SKILL_LOOKUP: dict[str, str] = {s.lower(): s for s in ALL_SKILLS}

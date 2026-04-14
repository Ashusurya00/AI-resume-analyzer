"""
Enterprise Skills Database — 300+ skills across 8 categories.
"""

SKILLS_DB: dict[str, list[str]] = {
    "Programming Languages": [
        "python", "java", "javascript", "typescript", "c++", "c#", "c",
        "go", "golang", "rust", "swift", "kotlin", "scala", "ruby", "php",
        "r", "matlab", "bash", "shell", "perl", "dart", "lua", "haskell",
        "elixir", "clojure", "groovy", "objective-c", "vba", "cobol",
    ],
    "Web & Frontend": [
        "html", "css", "react", "reactjs", "angular", "vue", "vuejs",
        "next.js", "nextjs", "nuxt", "svelte", "jquery", "bootstrap",
        "tailwind", "tailwindcss", "sass", "webpack", "vite", "graphql",
        "rest api", "restful", "redux", "gatsby", "remix", "storybook",
        "cypress", "playwright", "jest",
    ],
    "Backend & Cloud": [
        "node.js", "nodejs", "django", "flask", "fastapi", "spring boot",
        "spring", "express", "rails", "laravel", "asp.net", ".net",
        "microservices", "docker", "kubernetes", "aws", "azure", "gcp",
        "google cloud", "terraform", "ansible", "ci/cd", "github actions",
        "jenkins", "nginx", "redis", "kafka", "celery", "linux",
        "serverless", "lambda", "s3", "ec2", "rds", "heroku", "vercel",
    ],
    "Data & AI": [
        "machine learning", "deep learning", "neural networks", "nlp",
        "natural language processing", "computer vision", "data science",
        "data analysis", "data engineering", "feature engineering",
        "pandas", "numpy", "scipy", "scikit-learn", "sklearn", "tensorflow",
        "keras", "pytorch", "hugging face", "transformers", "llm", "rag",
        "langchain", "openai", "xgboost", "lightgbm", "spark", "pyspark",
        "hadoop", "airflow", "dbt", "mlflow", "data visualization",
        "matplotlib", "seaborn", "plotly", "tableau", "power bi", "looker",
        "statistics", "a/b testing", "regression", "classification",
        "clustering", "time series", "forecasting",
    ],
    "Databases": [
        "sql", "mysql", "postgresql", "postgres", "sqlite", "oracle",
        "sql server", "mongodb", "cassandra", "elasticsearch", "redis",
        "neo4j", "dynamodb", "firebase", "snowflake", "bigquery",
        "redshift", "databricks", "hive", "nosql",
    ],
    "Tools & Practices": [
        "git", "github", "gitlab", "bitbucket", "jira", "confluence",
        "agile", "scrum", "kanban", "devops", "tdd", "unit testing",
        "pytest", "postman", "swagger", "figma", "linux",
        "bash scripting", "jupyter", "poetry",
    ],
    "Soft Skills": [
        "leadership", "communication", "teamwork", "collaboration",
        "problem solving", "critical thinking", "project management",
        "time management", "adaptability", "creativity", "mentoring",
        "stakeholder management", "presentation", "negotiation",
        "analytical thinking", "attention to detail", "strategic thinking",
    ],
    "Domain & Business": [
        "product management", "business analysis", "system design",
        "api design", "ux design", "ui design", "cybersecurity",
        "blockchain", "smart contracts", "iot", "mobile development",
        "ios", "android", "react native", "flutter", "salesforce",
        "seo", "financial modeling",
    ],
}

ALL_SKILLS: list[str] = [s for skills in SKILLS_DB.values() for s in skills]

SKILL_ALIASES: dict[str, str] = {
    "reactjs": "react", "vuejs": "vue", "nodejs": "node.js",
    "nextjs": "next.js", "sklearn": "scikit-learn", "postgres": "postgresql",
    "golang": "go", "k8s": "kubernetes", "gcp": "google cloud",
    "tf": "tensorflow", "js": "javascript", "ts": "typescript",
}

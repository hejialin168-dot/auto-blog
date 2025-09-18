import os
import pandas as pd
import requests
import openai

# === 读取环境变量 ===
openai.api_key = os.getenv("OPENAI_API_KEY")
wp_user = os.getenv("WP_USER")
wp_pass = os.getenv("WP_APP_PASS")
wp_url = os.getenv("WP_URL").rstrip("/") + "/wp-json/wp/v2/posts"

print("DEBUG WP_URL:", wp_url)
print("DEBUG WP_USER:", wp_user)

# === 读取关键词文件 ===
df = pd.read_csv("keywords.csv")

# 每天只取一条（随机取一行）
row = df.sample(1).iloc[0]
keyword = row["keyword"]
lang = row["language"] if "language" in row and not pd.isna(row["language"]) else "en"

print(f"Generating blog for: {keyword} ({lang})")

# === 调用 OpenAI 生成内容 ===
prompt = f"Write a 1000-word SEO optimized blog post about '{keyword}' with headings and subheadings, in {lang}."
response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    max_tokens=1000,
    temperature=0.7
)

blog_text = response.choices[0].text.strip()
html_content = blog_text   # 避免 markdown 渲染错误

# === 发布到 WordPress ===
data = {
    "title": f"Blog about {keyword}",
    "content": html_content,
    "status": "publish"
}

r = requests.post(wp_url, auth=(wp_user, wp_pass), json=data)
print("Response:", r.status_code, r.text)

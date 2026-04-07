import os
import requests
import random

def post_pin():
    # Hna fine khass t-koun s-smya bhal GitHub Secrets nichan
    api_key = os.getenv('TMDB_API_KEY')
    token = os.getenv('PINTEREST_TOKEN') # Beddeltha 3la hsab t-tswira dyalk
    board_id = os.getenv('BOARD_ID')      # Beddeltha hta hya
    
    # 1. Njibo film
    m_type = random.choice(['movie', 'tv'])
    page = random.randint(1, 40)
    tmdb_url = f"https://api.themoviedb.org/3/{m_type}/popular?api_key={api_key}&page={page}"
    res = requests.get(tmdb_url).json()
    item = random.choice(res['results'])
    
    title = item.get('title') or item.get('name')
    slug = title.lower().replace(" ", "-").replace(":", "").replace("/", "")
    link = f"https://tomito.xyz/{m_type}/{item['id']}-{slug}"
    img = f"https://image.tmdb.org/t/p/w500{item['poster_path']}"

    # 2. Payload Pinterest
    payload = {
        "board_id": board_id,
        "title": title[:90],
        "description": f"Watch {title} on Tomito. #movies #streaming",
        "link": link,
        "media_source": {"source_type": "image_url", "url": img}
    }
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # 3. Post
    r = requests.post("https://api.pinterest.com/v5/pins", json=payload, headers=headers)
    
    print(f"Status: {r.status_code}")
    if r.status_code == 201:
        print(f"✅ Nadi! Posted: {title}")
    else:
        print(f"❌ Error: {r.text}")

if __name__ == "__main__":
    post_pin()

import os
import requests
import random

def get_random_tmdb_content():
    api_key = os.getenv('TMDB_API_KEY')
    # Khtar bin Movie awla TV show
    media_type = random.choice(['movie', 'tv'])
    # Khtar page random mn l-awal (page 1 tal 100 hit fihom popular content)
    page = random.randint(1, 100)
    
    url = f"https://api.themoviedb.org/3/{media_type}/popular?api_key={api_key}&page={page}"
    response = requests.get(url).json()
    
    if 'results' in response and len(response['results']) > 0:
        item = random.choice(response['results'])
        item['media_type'] = media_type
        return item
    return None

def post_to_pinterest():
    item = get_random_tmdb_content()
    if not item: return

    token = os.getenv('PINTEREST_TOKEN')
    board_id = os.getenv('BOARD_ID')
    
    m_type = item['media_type']
    item_id = item['id']
    title = item.get('title') or item.get('name')
    # Creer slug sghir
    slug = title.lower().replace(" ", "-").replace(":", "").replace("/", "")
    
    target_link = f"https://tomito.xyz/{m_type}/{item_id}-{slug}"
    image_url = f"https://image.tmdb.org/t/p/w500{item['poster_path']}"
    
    payload = {
        "board_id": board_id,
        "title": title[:90], # Pinterest limit 100 char
        "description": f"Watch {title} online on Tomito. {item.get('overview', '')[:150]}... #movies #tvshows #tomito",
        "link": target_link,
        "media_source": {
            "source_type": "image_url",
            "url": image_url
        }
    }
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    r = requests.post("https://api.pinterest.com/v5/pins", json=payload, headers=headers)
    print(f"Status: {r.status_code} | Posted: {title}")

if __name__ == "__main__":
    post_to_pinterest()

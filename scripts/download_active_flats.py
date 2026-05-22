import os
import urllib.request

flats_dir = "/Users/nathan/Daily Drip/public/assets/flats"
os.makedirs(flats_dir, exist_ok=True)

active_flats = {
    "flat_robot_front.png": "https://ivwgiw-k5.myshopify.com/cdn/shop/files/9226356700390701280_2048.jpg?v=1774737225&width=600",
    "flat_robot_back.png": "https://ivwgiw-k5.myshopify.com/cdn/shop/files/14890164672711313126_2048.jpg?v=1774737227&width=600",
    "flat_monkey_front.png": "https://ivwgiw-k5.myshopify.com/cdn/shop/files/14427770582284497701_2048.jpg?v=1774724955&width=600",
    "flat_monkey_back.png": "https://ivwgiw-k5.myshopify.com/cdn/shop/files/505426938446300089_2048.jpg?v=1774724956&width=600",
    "flat_peace_front.png": "https://ivwgiw-k5.myshopify.com/cdn/shop/files/8514859190100196355_2048.jpg?v=1775351979&width=600",
    "flat_peace_back.png": "https://ivwgiw-k5.myshopify.com/cdn/shop/files/8611523600852697158_2048.jpg?v=1775351981&width=600"
}

def download_flats():
    print("Downloading active flat-lay images from Shopify CDN...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    for filename, url in active_flats.items():
        dest = os.path.join(flats_dir, filename)
        print(f"Downloading {url} -> {dest}")
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response, open(dest, 'wb') as out_file:
                out_file.write(response.read())
            print(f"✅ Downloaded {filename} successfully.")
        except Exception as e:
            print(f"❌ Failed to download {filename}: {e}")

if __name__ == "__main__":
    download_flats()

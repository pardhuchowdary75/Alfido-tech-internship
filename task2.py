"""
============================================================
  Alfido Tech Internship – Task 2: API Integration & JSON Handling
  Author  : Intern
  Goal    : Fetch data from a public API, parse JSON, filter,
            search, and handle errors gracefully.
  API Used: https://jsonplaceholder.typicode.com  (free, no key)
            https://restcountries.com              (free, no key)
============================================================
"""

import requests
import json
from typing import Optional

BASE_POSTS    = "https://jsonplaceholder.typicode.com"
BASE_COUNTRIES = "https://restcountries.com/v3.1"

# ── Helper ───────────────────────────────────────────────────────────────────
def pretty(data) -> None:
    """Pretty-print any JSON-serialisable object."""
    print(json.dumps(data, indent=2, ensure_ascii=False))


def safe_get(url: str, params: Optional[dict] = None) -> Optional[dict | list]:
    """
    Perform a GET request with error handling.
    Returns parsed JSON or None on failure.
    """
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()           # raises HTTPError for 4xx/5xx
        return response.json()
    except requests.exceptions.ConnectionError:
        print(f"ERROR: Could not connect to {url}. Check internet connection.")
    except requests.exceptions.Timeout:
        print(f"ERROR: Request to {url} timed out.")
    except requests.exceptions.HTTPError as e:
        print(f"ERROR: HTTP {e.response.status_code} – {e.response.reason}")
    except requests.exceptions.JSONDecodeError:
        print("ERROR: Response is not valid JSON.")
    return None


# ============================================================
# SECTION 1 – Fetch all posts & show basic info
# ============================================================
def demo_fetch_posts() -> None:
    print("\n[1] Fetching posts from JSONPlaceholder…")
    posts = safe_get(f"{BASE_POSTS}/posts")
    if posts is None:
        return

    print(f"    Total posts fetched : {len(posts)}")
    print("    First 3 post titles :")
    for post in posts[:3]:
        print(f"      • [{post['id']}] {post['title']}")


# ============================================================
# SECTION 2 – Filter posts by userId
# ============================================================
def demo_filter_posts(user_id: int = 1) -> None:
    print(f"\n[2] Filtering posts for userId = {user_id}…")
    posts = safe_get(f"{BASE_POSTS}/posts", params={"userId": user_id})
    if posts is None:
        return

    print(f"    Posts found for user {user_id}: {len(posts)}")
    for p in posts[:2]:
        print(f"      Title : {p['title']}")
        print(f"      Body  : {p['body'][:80]}…\n")


# ============================================================
# SECTION 3 – Fetch single post and its comments
# ============================================================
def demo_post_with_comments(post_id: int = 5) -> None:
    print(f"\n[3] Fetching post #{post_id} and its comments…")

    post = safe_get(f"{BASE_POSTS}/posts/{post_id}")
    if post is None:
        return

    comments = safe_get(f"{BASE_POSTS}/posts/{post_id}/comments")
    if comments is None:
        return

    print(f"    Post   : {post['title']}")
    print(f"    Total comments : {len(comments)}")
    print("    First commenter emails:")
    for c in comments[:3]:
        print(f"      • {c['email']} → \"{c['name']}\"")


# ============================================================
# SECTION 4 – Search countries by name (restcountries API)
# ============================================================
def demo_search_country(name: str = "India") -> None:
    print(f"\n[4] Searching country info for '{name}'…")
    results = safe_get(f"{BASE_COUNTRIES}/name/{name}")
    if results is None:
        return

    country = results[0]   # take the best match
    info = {
        "Common Name"   : country.get("name", {}).get("common", "N/A"),
        "Official Name" : country.get("name", {}).get("official", "N/A"),
        "Capital"       : country.get("capital", ["N/A"])[0],
        "Region"        : country.get("region", "N/A"),
        "Population"    : f"{country.get('population', 0):,}",
        "Area (km²)"    : f"{country.get('area', 0):,.0f}",
        "Currency"      : list(country.get("currencies", {}).values())[0]["name"]
                          if country.get("currencies") else "N/A",
        "Languages"     : ", ".join(country.get("languages", {}).values()),
        "Timezone(s)"   : country.get("timezones", ["N/A"])[0],
    }
    for key, val in info.items():
        print(f"    {key:<18}: {val}")


# ============================================================
# SECTION 5 – Handle API errors on purpose (404)
# ============================================================
def demo_error_handling() -> None:
    print("\n[5] Demonstrating API error handling…")

    # 404 – post that doesn't exist
    print("    a) Requesting a non-existent post (id=9999)…")
    result = safe_get(f"{BASE_POSTS}/posts/9999")
    # JSONPlaceholder returns {} for missing items (still 200), handle it:
    if result == {}:
        print("       API returned empty object – resource likely not found.")
    elif result:
        print(f"       Got: {result}")

    # Bad endpoint → 404
    print("    b) Hitting a bad endpoint…")
    safe_get("https://jsonplaceholder.typicode.com/nonexistent_endpoint")

    # Unreachable host
    print("    c) Hitting an unreachable host…")
    safe_get("https://this-host-does-not-exist.example.com/api")


# ============================================================
# SECTION 6 – Save fetched data to JSON file
# ============================================================
def demo_save_to_json() -> None:
    print("\n[6] Saving fetched data to 'api_output.json'…")
    todos = safe_get(f"{BASE_POSTS}/todos", params={"userId": 1})
    if todos is None:
        return

    # Keep only completed ones as a demo filter
    completed = [t for t in todos if t["completed"]]
    output = {
        "source"   : f"{BASE_POSTS}/todos?userId=1",
        "total"    : len(todos),
        "completed": len(completed),
        "items"    : completed,
    }

    filepath = "api_output.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"    Saved {len(completed)} completed todos → {filepath}")


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  Alfido Tech – Task 2: API Integration & JSON Handling")
    print("=" * 60)

    demo_fetch_posts()
    demo_filter_posts(user_id=2)
    demo_post_with_comments(post_id=3)
    demo_search_country("India")
    demo_error_handling()
    demo_save_to_json()

    print("\n" + "=" * 60)
    print("  Task 2 Complete ✓")
    print("=" * 60)
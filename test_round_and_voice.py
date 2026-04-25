import requests
import io
import time

BASE_URL = "http://localhost:8000"

def test_flow():
    print("1. Fetching courses...")
    resp = requests.get(f"{BASE_URL}/courses/")
    assert resp.status_code == 200, f"Failed to get courses: {resp.text}"
    data = resp.json()
    assert data["success"], "Success flag false"
    courses = data["data"]
    if not courses:
        print("No courses found. Cannot continue test.")
        return
    course_id = courses[0]["id"]
    print(f"   Selected course_id: {course_id}")
    
    print("\n2. Creating a new round...")
    round_payload = {
        "course_id": course_id,
        "date": "2026-04-25T10:00:00Z",
        "players": ["A", "B", "C", "D"]
    }
    resp = requests.post(f"{BASE_URL}/rounds/", json=round_payload)
    assert resp.status_code == 200, f"Failed to create round: {resp.text}"
    data = resp.json()
    round_id = data["data"]["id"]
    print(f"   Created round_id: {round_id}")
    
    print("\n3. Testing Voice Command: '1번홀 파4 A 스코어 5'")
    # Create fake audio file
    fake_audio = io.BytesIO(b"fake audio data")
    fake_audio.name = "voice.webm"
    files = {"file": ("voice.webm", fake_audio, "audio/webm")}
    resp = requests.post(f"{BASE_URL}/voice/upload", files=files)
    assert resp.status_code == 200, f"Failed voice upload: {resp.text}"
    data = resp.json()
    
    print(f"   Voice parsed text: {data['data']['text']}")
    parsed = data["data"]["parsed"]
    print(f"   Parsed data: {parsed}")
    
    # Ensure our mock worked
    assert parsed["hole_number"] == 1
    assert parsed["par"] == 4
    
    print("\n4. Updating Hole 1 score using parsed voice data...")
    hole_number = parsed["hole_number"]
    patch_payload = parsed.get("scores", {})
    params = {}
    if "par" in parsed:
        params["par"] = parsed["par"]
        
    resp = requests.patch(f"{BASE_URL}/rounds/{round_id}/holes/{hole_number}", json=patch_payload, params=params)
    assert resp.status_code == 200, f"Failed to update hole: {resp.text}"
    print("   Hole 1 successfully updated!")
    
    print("\n5. Fetching Round Detail to verify...")
    resp = requests.get(f"{BASE_URL}/rounds/{round_id}")
    assert resp.status_code == 200
    round_data = resp.json()
    scores = round_data["data"]["scores"]
    
    # find hole 1
    hole_1 = next((h for h in scores if h["hole_number"] == 1), None)
    print(f"   Hole 1 current state: {hole_1}")
    assert hole_1["score_a"] == 5, f"Expected A score to be 5, got {hole_1['score_a']}"
    assert hole_1["score_b"] == 4, f"Expected B score to be 4, got {hole_1['score_b']}"
    
    print("\n✅ All verifications passed successfully!")

if __name__ == "__main__":
    try:
        test_flow()
    except Exception as e:
        print(f"❌ Test Failed: {e}")

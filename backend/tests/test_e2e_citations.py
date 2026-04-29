import asyncio
import httpx
import uuid

async def test_e2e():
    try:
        # User ID MUST be a valid UUID. Using a dummy but valid UUID for test if user does not exist.
        test_uuid = str(uuid.uuid4())
        print(f"Testing with User ID: {test_uuid}")
        
        async with httpx.AsyncClient() as client:
            # Note: We need a real user in the DB for /citations to work without 404, check main.py.
            # Instead of going through full registration, we can just hit a generic health check or bypass db user requirement by mocking.
            
            # Since user needs to be in DB, let's register a temporary user for the test.
            register_payload = {
                "name": "Test User",
                "age": 30,
                "gender": "male",
                "mbti": "ENTP",
                "goal_type": "weight_loss",
                "goal_description": "Lose 5kg",
                "start_weight": 80.0,
                "target_weight": 75.0,
                "wake_time": "07:00",
                "sleep_time": "23:00",
                "is_consented": True
            }
            
            print("\n--- 1. Registering Test User ---")
            reg_res = await client.post("http://127.0.0.1:8000/v1/users/register", json=register_payload)
            if reg_res.status_code != 200:
                print(f"Failed to register: {reg_res.status_code} - {reg_res.text}")
                return
            
            user_id = reg_res.json().get("user_id")
            print(f"User registered successfully! ID: {user_id}")
            
            print("\n--- 2. Fetching Citations (E2E #11 Feature) ---")
            citations_res = await client.get(f"http://127.0.0.1:8000/v1/coach/citations", params={"user_id": user_id, "query": "weight loss management"})
            print(f"Status Code: {citations_res.status_code}")
            data = citations_res.json()
            
            citations = data.get("citations", [])
            total = data.get("total", 0)
            print(f"Total Citations Found: {total}")
            
            for i, c in enumerate(citations, 1):
                print(f"\n[Citation {i}]")
                print(f"Title   : {c.get('title')}")
                print(f"Authors : {c.get('authors')}")
                print(f"Journal : {c.get('journal')}")
                print(f"DOI     : {c.get('doi')}")
                print(f"Excerpt : {c.get('excerpt')}")
                
            print("\nE2E Test Completed Successfully!")
            
    except Exception as e:
        print(f"Error during E2E test: {e}")

if __name__ == "__main__":
    asyncio.run(test_e2e())

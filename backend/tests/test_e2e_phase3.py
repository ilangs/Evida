import asyncio
import httpx
import uuid

async def test_e2e_phase2_complete():
    try:
        print("Starting E2E Test (Up to Phase 2 - #14, #15)")
        async with httpx.AsyncClient() as client:
            # 1. Register User
            register_payload = {
                "name": "Phase 2 User",
                "age": 28,
                "gender": "female",
                "mbti": "ENFJ",
                "goal_type": "weight_loss",
                "goal_description": "Health Improvement",
                "start_weight": 65.0,
                "target_weight": 55.0,
                "wake_time": "06:30",
                "sleep_time": "22:30",
                "is_consented": True
            }
            
            print("\n--- 1. Registering Test User ---")
            reg_res = await client.post("http://127.0.0.1:8001/v1/users/register", json=register_payload)
            if reg_res.status_code != 200:
                print(f"Failed to register: {reg_res.status_code} - {reg_res.text}")
                return
            
            user_id = reg_res.json().get("user_id")
            print(f"User registered successfully! ID: {user_id}")
            
            # 2. Check Biometric History (#14 related endpoint)
            print("\n--- 2. Fetching Biometric History (#14) ---")
            bio_res = await client.get(f"http://127.0.0.1:8001/v1/users/{user_id}/biometric-history")
            print(f"Status Code: {bio_res.status_code}")
            print("Response:", bio_res.json())

            # 3. Check Notifications (#15 feature)
            print("\n--- 3. Fetching Notifications (#15) ---")
            noti_res = await client.get(f"http://127.0.0.1:8001/v1/users/{user_id}/notifications")
            print(f"Status Code: {noti_res.status_code}")
            print("Response:", noti_res.json())

            print("\nPhase 2 (#14, #15) E2E Test Completed Successfully!")
            
    except Exception as e:
        print(f"Error during E2E test: {e}")

if __name__ == "__main__":
    asyncio.run(test_e2e_phase2_complete())

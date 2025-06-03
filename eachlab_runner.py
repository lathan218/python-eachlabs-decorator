import requests
from functools import wraps
import time

def eachlab_runner(api_key, model, version):
    def decorator(func):
        @wraps(func)
        def eachlab_wrapper(*args, **kwargs):
            base_url = 'https://api.eachlabs.ai/v1/prediction/'
            response = requests.post(
                base_url,
                headers={
                    "X-API-KEY": api_key,
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "version": version,
                    "input": func(*args, **kwargs)
                },
            )

            try:
                prediction_data = response.json()
                print("Initial response:", prediction_data)
                if prediction_data.get('status') != 'success':
                    return {'status': 'error'}
            except:
                return {'status': 'error'}

            prediction_id = prediction_data["predictionID"]
            while True:
                result = requests.get(
                    f"{base_url}{prediction_id}",
                    headers={"X-API-KEY": api_key},
                ).json()

                if result["status"] in ["success", "error", "cancelled"]:
                    print("Final result:", result)
                    break

                print("Still processing...")
                time.sleep(5)
            return result
        return eachlab_wrapper
    return decorator

@eachlab_runner('EACHLABS_API_KEY', "flux-1-1-pro", "0.0.1")
def flux1_1pro(prompt = '', width = 1024, height = 768, seed = 42):
    input_data = {
        "prompt_upsampling": False,
        "seed": seed,
        "width": width,
        "height": height,
        "prompt": prompt,
        "output_format": "png",
        "safety_tolerance": 2
    }

    return input_data

if __name__ == '__main__':
    result = flux1_1pro("Generate a beautiful modern style living room", 1440, 820, 1234)
    print(result)
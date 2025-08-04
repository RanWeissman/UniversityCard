import requests

# Your API endpoint
url = "http://127.0.0.1:8000/generate"  # or use "http://myapp.local:8000/" if you've mapped it

# Form data
data = {
    "name": "John Johnson",
    "id_number": "5353535353"
}

# File upload (adjust file path to a real image on your system)
files = {"file": ("profile_photo.jpg", open("C:\\Users\\Ran\\Desktop\\Ran\\Projects\\UniCard\\profile_photo.jpg", "rb"),
                  "image/jpeg")}

response = requests.post(url, data=data, files=files)

print("Status Code:", response.status_code)
print("Response Text:", response.text)

import http.client

def check_http_status():
    conn = http.client.HTTPConnection("localhost", 80)
    conn.request("GET", "/accounts/login/")
    response = conn.getresponse()
    
    if response.status == 200:
        print("HTTP request succeeded (Status 200 OK).")
    else:
        raise ValueError(f"HTTP request failed with status code: {response.status}")


if __name__ == "__main__":
    try:
        check_http_status()
    except Exception as e:
        print(str(e))
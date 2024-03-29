# This program makes an HTTP request to the server to check if it is running properly, then it returns a custom error
# based off of what when wrong. 
import http.client

def check_http_status():
    global response
    conn = http.client.HTTPConnection("localhost", 80)
    conn.request("GET", "/accounts/login/")
    response = conn.getresponse()
    
    assert response.status == 200


if __name__ == "__main__":
    try:
        check_http_status()
    except AssertionError:
        raise AssertionError('Status code is not 200. Status code is: ' + str(response.status))
    except ConnectionRefusedError:
        raise ConnectionRefusedError('the response failed')
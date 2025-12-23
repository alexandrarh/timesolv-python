# TimeSolv Python API
Package that allows for Python-friendly usage of <a href="https://apps.timesolv.com/Services/rest/oauth2v1/">TimeSolv's REST API</a>. Made for primary usage of timekeeping and employee tracking within the TimeSolv system.

## Prerequisites
Below are the necessary components that need to be provided by the user when using the package. 
- Python 3.12+
- TimeSolv firm **and** developer account
- `pip` installation tool

## Installation
To install `timesolv_api` onto your Python environment, paste the following command in your terminal (refer to the OS listed).

### Unix/macOS
```bash
python3 -m pip install timesolv_api
```

### Windows
```bash
py -m pip install timesolv_api
```

### NOTE
Though not required, it's *highly recommended* that `timesolv_api` is installed on a virtual environemnt wherever it's going to be used. To create <u>and</u> activate the virtual environment, use the following commands (refer to the OS listed).

#### Unix/macOS
```bash
python3 -m venv .venv
```

#### Windows
```bash
py -m venv .venv
```

## Configuration
In order to utilize the `timesolv_api` package, you will need the following variables.
- `client_id`
- `client_secret`
- `redirect_uri`
- `auth_code`

These components are obtained via TimeSolv's **developer** account settings. To set these up, please refer to <a href='https://help.timesolv.com/connect-to-timesolv-with-rest-api'>TimeSolv's developer account setup documentation</a>.

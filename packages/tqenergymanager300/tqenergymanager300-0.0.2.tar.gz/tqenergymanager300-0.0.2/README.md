# TQ-Automation Energy Manager 300

Python library to request data from TQ-Automation Energy Manager EM300 (aka B-control Energy Manager EM-300 aka Kostal EM300LR).

Usage:
```python
import tqenergymanager300

client = TqEnergyManagerJsonClient(
	"192.168.251.22", "12345678", "Password"
)
logged_in = client.login()
if logged_in:
	print(client.fetch_data())
```

Special thanks to Kilian Knoll for an [example project](https://github.com/kilianknoll/EM300) how to access the API.

This project is not affiliated with TQ-Systems GmbH or any of its affiliates.

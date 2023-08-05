# Feature Flags Backend Client

pip install feature_flags_client

```
from flags_be_client import FeatureFlagClient

ff = FeatureFlagClient()

def is_flag_enabled(optional_identifier):
    return ff.is_enabled("exact_flag_name", optional_identifier)
```
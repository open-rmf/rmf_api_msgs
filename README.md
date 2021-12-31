# rmf_api_msgs

Collection of json message schemas which bridges the C++ and python components of RMF to the web interface

# Usage

Compile with [colcon](https://colcon.readthedocs.io/en/released/) is recommended

```bash
colcon build --packages-select rmf_api_msgs
source install/setup.bash
```

Subsequently, to access the schemas, the user just needs to include/import the cpp header or py module into their source code.

1. C++ example:

```cpp
#include <rmf_api_msgs/schemas/task_state.hpp>

nlohmann::json schema = rmf_api_msgs::schemas::task_state
```

1. Python example:

```py
from rmf_api_msgs import schemas

schema = schemas.task_state()
```

from pydantic import BaseModel

class LocustUserConfig(BaseModel):
    wait_time_min: float = 1
    wait_time_max: float = 3
from pydantic import BaseModel


class ApiSchema(BaseModel):
    model_config = {"from_attributes": True}

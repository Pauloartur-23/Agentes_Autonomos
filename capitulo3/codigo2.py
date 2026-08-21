from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider


class CityLocation(BaseModel):
    city: str
    country: str


ollama_model = OpenAIChatModel(
    "gpt-oss:20b",
    provider=OllamaProvider(
        base_url="http://localhost:11434/v1"
    ),
)


agent = Agent(
    model=ollama_model,
    output_type=CityLocation
)


result = agent.run_sync(
    "Onde foi a olimpíada de 2012?"
)


print(result.output)
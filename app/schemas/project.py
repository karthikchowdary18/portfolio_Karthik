from pydantic import BaseModel, ConfigDict, Field


class ProjectBase(BaseModel):
    title_en: str = Field(..., min_length=1, max_length=160)
    title_de: str = Field(..., min_length=1, max_length=160)
    summary_en: str = Field(..., min_length=1)
    summary_de: str = Field(..., min_length=1)
    impact_en: str = Field(..., min_length=1)
    impact_de: str = Field(..., min_length=1)
    tech_stack: list[str] = Field(default_factory=list)
    timeframe: str = Field(..., min_length=1, max_length=80)
    category: str = Field(..., min_length=1, max_length=80)
    featured: bool = False
    live_url: str = ""
    repo_url: str = ""


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

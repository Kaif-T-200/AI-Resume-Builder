from typing import List, Optional
from pydantic import BaseModel, Field


class Contact(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    links: List[str] = Field(default_factory=list)


class Experience(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    current: bool = False
    bullets: List[str] = Field(default_factory=list)
    technologies: List[str] = Field(default_factory=list)
    employment_type: Optional[str] = None


class Education(BaseModel):
    institution: Optional[str] = None
    degree: Optional[str] = None
    field: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    gpa: Optional[str] = None


class Project(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    bullets: List[str] = Field(default_factory=list)
    stack: List[str] = Field(default_factory=list)
    link: Optional[str] = None
    outcome: Optional[str] = None


class Certification(BaseModel):
    name: Optional[str] = None
    issuer: Optional[str] = None
    date_obtained: Optional[str] = None
    credential_id: Optional[str] = None


class Resume(BaseModel):
    contact: Contact
    summary: Optional[str] = None
    experience: List[Experience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    certifications: List[Certification] = Field(default_factory=list)
    achievements: List[str] = Field(default_factory=list)
    extracurricular: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    interests: List[str] = Field(default_factory=list)


class CoverLetter(BaseModel):
    contact: Contact
    body: str


class TemplateMetadata(BaseModel):
    name: str
    description: str
    sections: List[str]

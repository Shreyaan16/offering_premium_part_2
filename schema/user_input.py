from typing import Literal , Annotated
from pydantic import BaseModel , Field , computed_field , field_validator
from config.city_tier import tier_1_cities , tier_2_cities

class UserInput(BaseModel):
    age: Annotated[int , Field(... , gt = 0 , lt = 100 , description = "Age of the user")]
    weight: Annotated[float , Field(... , gt = 0 , description = "Weight of the user")]
    height: Annotated[float , Field(... , gt = 0 , description = "Height of the user")]
    income_lpa: Annotated[float , Field(... , description = "Income of the user in lpa")]
    smoker: Annotated[bool , Field(... , description = "Is user a smoker")]
    city: Annotated[str ,  Field(... , description = "City of the user")]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
                                'business_owner', 'unemployed', 'private_job'], Field(..., description='Occupation of the user')]
    
    @field_validator('city')
    @classmethod
    def title_city(cls , value : str) -> str:
        value = value.strip().title()
        return value

    
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
        
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / ((self.height)**2)
    
    @computed_field
    @property
    def risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif (self.smoker and self.bmi > 27) or (not self.smoker and self.bmi > 27):
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age >=25 and self.age < 45:
            return "adult"
        elif self.age >= 45 and self.age < 60:
            return "middle_aged"
        else:
            return "senior"
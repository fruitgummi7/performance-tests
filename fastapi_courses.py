from fastapi import FastAPI, APIRouter, status, HTTPException
from pydantic import BaseModel, EmailStr, RootModel

app = FastAPI()

courses_router = APIRouter(
    prefix="/api/v1/courses",
    tags=["courses-service"]
)

class CourseIn(BaseModel):
    title: str
    max_score: int
    min_score: int
    description: str

class CourseOut(CourseIn):
    id: int


class CoursesStore(RootModel):
    root: list[CourseOut]

    def find(self, course_id: int) -> CourseOut | None:
        return next(filter(lambda course: course.id == course_id, self.root), None)

    def create(self, course_in: CourseIn) -> CourseOut:
        course = CourseOut(id=len(self.root) +1, **course_in.model_dump())
        self.root.append(course)
        return course

    def update(self, course_id: int, course_in: CourseIn) -> CourseOut:
        index = next(index for index, course in enumerate(self.root) if course.id == course_id)
        updated = CourseOut(id=course_id, **course_in.model_dump())
        self.root[index] = updated
        return updated

    def delete(self, course_id: int) -> None:
        self.root = [course for course in self.root if course.id != course_id]


store = CoursesStore(root=[])

@courses_router.get("", response_model=list[CourseOut])
async def get_courses():
    return store.root

@courses_router.get("/{course_id}", response_model=CourseOut)
async def get_course(course_id: int):
    if not (course := store.find(course_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    return course

@courses_router.post("", response_model=CourseOut)
async def create_course(course: CourseIn):
    return store.create(course)

@courses_router.put("/{course_id}", response_model=CourseOut)
async def update_course(course_id: int, course: CourseIn):
    if not store.find(course_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    return store.update(course_id, course)

@courses_router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int):
    if not store.find(course_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    return store.delete(course_id)

app.include_router(courses_router)
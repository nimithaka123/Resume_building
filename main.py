from urllib import request
from database import Session
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import PlainTextResponse, JSONResponse
from datetime import datetime
from models import (
    Basic_Details,
    Education,
    Location,
    Project_Details,
    Skills,
    Social_Media,
    Work_Experience,
)
import validation
import json

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

middleware = [Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])]

db = Session()


# ****************List all resume*******************
async def get_all_resume(request: Request):
    basic_details_from_database = (
        db.query(Basic_Details).order_by(Basic_Details.basic_details_id.desc()).all()
    )
    basic_details_content = [
        {k: v for k, v in vars(basic_detail).items() if k != "_sa_instance_state"}
        for basic_detail in basic_details_from_database
    ]
    # converting type of applied_date to string
    basic_details_content = [
        {k: str(v) if k == "applied_date" else v for k, v in content.items()}
        for content in basic_details_content
    ]
    return JSONResponse({"data": basic_details_content}, status_code=200)


# ********************Search by name or email***************************
async def search_by_name_or_email(request: Request):
    search_by_condition = request.path_params.get("query")
    basic_details_from_database = (
        db.query(Basic_Details)
        .filter(
            (Basic_Details.name.like("%" + search_by_condition + "%"))
            | (Basic_Details.email.like("%" + search_by_condition + "%"))
        )
        .all()
    )
    basic_details_content = [
        {k: v for k, v in vars(basic_details).items() if k != "_sa_instance_state"}
        for basic_details in basic_details_from_database
    ]
    content = [
        {k: str(v) if k == "applied_date" else v for k, v in content.items()}
        for content in basic_details_content
    ]
    return JSONResponse({"data": content}, status_code=200)


# **************delete the resume*************
async def delete_resume(request: Request):
    id_to_be_deleted = request.path_params.get("applicant_id")
    data_to_be_deleted = db.query(Basic_Details).filter(
        Basic_Details.basic_details_id == id_to_be_deleted
    )
    data_to_be_deleted.delete()
    db.commit()
    return JSONResponse({"data": "deleted"})


# ******Functions for accessing data from each table*************


def get_basic_details(id):
    basic_details_from_database = (
        db.query(Basic_Details).filter(Basic_Details.basic_details_id == id).all()
    )
    database_content = [
        {k: v for k, v in vars(basic_detail).items() if k != "_sa_instance_state"}
        for basic_detail in basic_details_from_database
    ]
    database_content = [
        {k: str(v) if k == "applied_date" else v for k, v in content.items()}
        for content in database_content
    ]
    return database_content


def get_location_details(id):
    location_details_from_database = (
        db.query(Location).filter(Location.basic_details_id == id).all()
    )
    location_content = [
        {k: v for k, v in vars(location).items() if k != "_sa_instance_state"}
        for location in location_details_from_database
    ]
    return location_content


def get_education_details(id):
    education_details_from_database = (
        db.query(Education).filter(Education.basic_details_id == id).all()
    )
    education_content = [
        {k: v for k, v in vars(education).items() if k != "_sa_instance_state"}
        for education in education_details_from_database
    ]
    education_content = [
        {k: str(v) if k in ["start_date", "end_date"] else v for k, v in cont.items()}
        for cont in education_content
    ]
    return education_content


def get_work_experience_details(id):
    work_experience_details_from_database = (
        db.query(Work_Experience).filter(Work_Experience.basic_details_id == id).all()
    )
    experience_content = [
        {k: v for k, v in vars(experience).items() if k != "_sa_instance_state"}
        for experience in work_experience_details_from_database
    ]
    experience_content = [
        {k: str(v) if k in ["start_date", "end_date"] else v for k, v in cont.items()}
        for cont in experience_content
    ]
    return experience_content


def get_project_details(id):
    project_details_from_database = (
        db.query(Project_Details).filter(Project_Details.basic_details_id == id).all()
    )
    project_content = [
        {k: v for k, v in vars(project).items() if k != "_sa_instance_state"}
        for project in project_details_from_database
    ]
    return project_content


def get_skill_details(id):
    skill_details_from_database = (
        db.query(Skills).filter(Skills.basic_details_id == id).all()
    )
    skill_content = [
        {k: v for k, v in vars(skill).items() if k != "_sa_instance_state"}
        for skill in skill_details_from_database
    ]
    return skill_content


def get_social_media_details(id):
    social_media_details_from_database = (
        db.query(Social_Media).filter(Social_Media.basic_details_id == id).all()
    )
    social_media_content = [
        {k: v for k, v in vars(social_media).items() if k != "_sa_instance_state"}
        for social_media in social_media_details_from_database
    ]
    return social_media_content


# ******************** get individual resume************************
async def get_individual_resume(request: Request):
    id = request.path_params.get("applicant_id")
    if request.method == "GET":
        return JSONResponse(
            {
                "basic_details": get_basic_details(id),
                "location_details": get_location_details(id),
                "education_details": get_education_details(id),
                "work_experience_details": get_work_experience_details(id),
                "project_details": get_project_details(id),
                "skill_details": get_skill_details(id),
                "social_media_details": get_social_media_details(id),
            }
        )


# ********************create new resume*******************


async def create_new_resume(request: Request):
    if request.method == "POST":
        data_to_be_added = await request.json()
        location_details = data_to_be_added.pop("location_details")
        education_details = data_to_be_added.pop("education_details")
        work_experience_details = data_to_be_added.pop("work_experience")

        project_details = data_to_be_added.pop("project_details")
        skill_details = data_to_be_added.pop("skills")
        social_media_details = data_to_be_added.pop("social_media")
        new_basic_details_data = Basic_Details(**data_to_be_added)
        try:
            validation.Basic_Details.from_orm(new_basic_details_data)
            db.add(new_basic_details_data)
            db.commit()
            db.refresh(new_basic_details_data)
        except Exception as e:
            print(e)
            return JSONResponse({"Error: ": f"{e}"}, status_code=400)

        basic_details_id = db.query(Basic_Details.basic_details_id).all()
        max_basic_details_id = max([i for ik in basic_details_id for i in ik])

        for location in location_details:
            location["basic_details_id"] = max_basic_details_id
        for education in education_details:
            education["basic_details_id"] = max_basic_details_id
            if "start_date" in education.keys() and not education["start_date"]:
                education.pop("start_date", "")
            if "end_date" in education.keys() and not education["end_date"]:
                education.pop("end_date", "")
        for experience in work_experience_details:
            experience["basic_details_id"] = max_basic_details_id
            if "start_date" in experience.keys() and not experience["start_date"]:
                experience.pop("start_date", "")
            if "end_date" in experience.keys() and not experience["end_date"]:
                experience.pop("end_date", "")
        for project in project_details:
            project["basic_details_id"] = max_basic_details_id
        for skill in skill_details:
            skill["basic_details_id"] = max_basic_details_id
        for social_media in social_media_details:
            social_media["basic_details_id"] = max_basic_details_id

        new_location_details = [Location(**i) for i in location_details]
        new_education_details = [Education(**i) for i in education_details]
        new_experience_details = [Work_Experience(**i) for i in work_experience_details]
        new_project_details = [Project_Details(**i) for i in project_details]
        new_skill_details = [Skills(**i) for i in skill_details]
        new_social_media_details = [Social_Media(**i) for i in social_media_details]

        try:

            db.add_all(new_location_details)
            db.add_all(new_education_details)
            db.add_all(new_experience_details)
            db.add_all(new_project_details)
            db.add_all(new_skill_details)
            db.add_all(new_social_media_details)
            db.commit()
            return JSONResponse({"data": "inserted"}, status_code=200)

        except Exception as e:
            db.rollback()
            print(e)
            return


# ******************update individual resume**************


async def update_individual_resume(request: Request):

    if request.method == "PUT":
        id = request.path_params.get("applicant_id")
        update_data = await request.json()
        basic = update_data.pop("basic_details")
        location = update_data.pop("location_details")
        education = update_data.pop("education_details")
        experience = update_data.pop("work_experience_details")
        project = update_data.pop("project_details")
        skills = update_data.pop("skill_details")
        social_media = update_data.pop("social_media_details")

        try:
            for bas in basic:
                basic_details_db = db.query(Basic_Details).filter(
                    Basic_Details.basic_details_id == id
                )
                basic_details_db.update(bas, synchronize_session=False)
                db.commit()

            for loc in location:
                if "location_id" in loc.keys():
                    location_details_db = db.query(Location).filter(
                        (Location.basic_details_id == id)
                        & (Location.location_id == loc["location_id"])
                    )
                    location_details_db.update(loc, synchronize_session=False)
                    db.commit()
                else:
                    loc["basic_details_id"] = id
                    new_location = Location(**loc)
                    db.add(new_location)
                    db.commit()
            house_names = [sub["address"] for sub in location]
            house_name_db = (
                db.query(Location.address)
                .filter((Location.basic_details_id == id))
                .all()
            )
            house_names_from_database = [lis[0] for lis in house_name_db]
            for name in house_names_from_database:
                if name not in house_names:
                    data_delete = db.query(Location).filter(Location.address == name)
                    data_delete.delete()
                    db.commit()

            for edu in education:
                if "start_date" in edu.keys() and not edu["start_date"]:
                    education.pop("start_date", "")
                if "end_date" in edu.keys() and not edu["end_date"]:
                    education.pop("end_date", "")

                if "education_details_id" in edu.keys():
                    education_details_db = db.query(Education).filter(
                        (Education.basic_details_id == id)
                        & (
                            Education.education_details_id
                            == edu["education_details_id"]
                        )
                    )
                    education_details_db.update(edu, synchronize_session=False)
                    db.commit()
                else:
                    edu["basic_details_id"] = id
                    new_education = Education(**edu)
                    db.add(new_education)
                    db.commit()

            qualification = [sub["qualification"] for sub in education]
            qualification_db = (
                db.query(Education.qualification)
                .filter((Education.basic_details_id == id))
                .all()
            )
            qualification_from_database = [lis[0] for lis in qualification_db]
            for q in qualification_from_database:
                if q not in qualification:
                    data_delete = db.query(Education).filter(
                        Education.qualification == q
                    )
                    data_delete.delete()
                    db.commit()

            for exp in experience:
                if "experience_details_id" in exp.keys():
                    experience_details_db = db.query(Work_Experience).filter(
                        (Work_Experience.basic_details_id == id)
                        & (
                            Work_Experience.experience_details_id
                            == exp["experience_details_id"]
                        )
                    )
                    experience_details_db.update(exp, synchronize_session=False)
                    db.commit()

                else:
                    exp["basic_details_id"] = id
                    new_work_experience = Work_Experience(**exp)
                    db.add(new_work_experience)
                    db.commit()
            job_roles = [sub["job_role"] for sub in experience]
            job_roles_db = (
                db.query(Work_Experience.job_role)
                .filter((Work_Experience.basic_details_id == id))
                .all()
            )
            job_roles_from_database = [lis[0] for lis in job_roles_db]
            for j in job_roles_from_database:
                if j not in job_roles:
                    data_delete = db.query(Work_Experience).filter(
                        Work_Experience.job_role == j
                    )
                    data_delete.delete()
                    db.commit()

            for pro in project:
                if "project_details_id" in pro.keys():
                    project_details_db = db.query(Project_Details).filter(
                        (Project_Details.basic_details_id == id)
                        & (
                            Project_Details.project_details_id
                            == pro["project_details_id"]
                        )
                    )
                    project_details_db.update(pro, synchronize_session=False)
                    db.commit()

                else:
                    pro["basic_details_id"] = id
                    new_project = Project_Details(**pro)
                    db.add(new_project)
                    db.commit()
            project_titles = [sub["project_title"] for sub in project]
            project_titles_db = (
                db.query(Project_Details.project_title)
                .filter((Project_Details.basic_details_id == id))
                .all()
            )
            project_titles_from_database = [lis[0] for lis in project_titles_db]
            for project_title in project_titles_from_database:
                if project_title not in project_titles:
                    data_delete = db.query(Project_Details).filter(
                        Project_Details.project_title == project_title
                    )
                    data_delete.delete()
                    db.commit()

            skill_names_in_data_to_be_edited = [sub["skill_name"] for sub in skills]
            skills_name_db = (
                db.query(Skills.skill_name)
                .filter((Skills.basic_details_id == id))
                .all()
            )
            # converting list of tuples to list of elements
            skill_names_from_database = [lis[0] for lis in skills_name_db]
            for skill_name in skill_names_in_data_to_be_edited:
                if skill_name not in skill_names_from_database:
                    for skill in skills:
                        if "skills_id" in skill.keys():
                            skills_details_db = db.query(Skills).filter(
                                (Skills.basic_details_id == id)
                                & (Skills.skills_id == skill["skills_id"])
                            )
                            skills_details_db.update(skill, synchronize_session=False)
                            db.commit()
                        else:
                            skill["basic_details_id"] = id
                            new_skill = Skills(**skill)
                            db.add(new_skill)
                            db.commit()
            for skill_name in skill_names_from_database:
                if skill_name not in skill_names_in_data_to_be_edited:
                    data_delete = db.query(Skills).filter(
                        Skills.skill_name == skill_name
                    )
                    print("delete", data_delete)
                    data_delete.delete()
                    db.commit()

            for soc in social_media:
                if "social_media_id" in soc.keys():
                    social_media_db = db.query(Social_Media).filter(
                        (Social_Media.basic_details_id == id)
                        & (Social_Media.social_media_id == soc["social_media_id"])
                    )
                    social_media_db.update(soc, synchronize_session=False)
                    db.commit()
                else:
                    soc["basic_details_id"] = id
                    new_social_media = Social_Media(**soc)
                    db.add(new_social_media)
                    db.commit()
            social_media_urls = [sub["url"] for sub in social_media]
            social_media_urls_db = (
                db.query(Social_Media.url)
                .filter((Social_Media.basic_details_id == id))
                .all()
            )
            social_media_urls_from_database = [lis[0] for lis in social_media_urls_db]
            for url in social_media_urls_from_database:
                if url not in social_media_urls:
                    data_delete = db.query(Social_Media).filter(Social_Media.url == url)
                    data_delete.delete()
                    db.commit()
            return JSONResponse({"data": "updated successfully"})

        except Exception as e:
            print("Error: ", e)
            db.rollback()


routes = [
    Route("/all-resume", endpoint=get_all_resume),
    Route("/resume/{query:str}/", endpoint=search_by_name_or_email),
    Route(
        "/individual-resume/{applicant_id:int}/",
        endpoint=get_individual_resume,
        methods=["GET"],
    ),
    Route("/new-resume", endpoint=create_new_resume, methods=["GET", "POST"]),
    Route(
        "/update-individual-resume/{applicant_id:int}/",
        endpoint=update_individual_resume,
        methods=["PUT"],
    ),
    Route("/resume/{applicant_id:int}/", endpoint=delete_resume, methods=["DELETE"]),
]

app = Starlette(debug=True, routes=routes, middleware=middleware)

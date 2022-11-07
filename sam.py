# from database import Session,engine
# from models import Basic_Details

# local_session=Session(bind=engine)

# def create_a_resume(resume_data):

#     new_resume=Basic_Details(**resume_data)

#     try:
#         local_session.add(new_resume)
#         local_session.commit()
#         local_session.refresh(new_resume)

#     except Exception as e:
        # local_session.rollback()
        # print(e)
    # finally:
    #     local_session.close()

# def get_a_applicant_by_id(applicant_id):
#     return local_session.query(Basic_Details).filter(Basic_Details.id==applicant_id).first()


# def update_student_data(student_id,student_data):
#     student_to_update=get_a_student_by_id(student_id)
#     student_to_update.name = student_data["name"]
#     student_to_update.address =student_data["addr experience_content = [{k:str(v) if k ess"]

#     local_session.commit()


# def delete_student_data(student_id):
#     student_to_delete=get_a_student_by_id(student_id)

#     local_session.delete(student_to_delete)

#     local_session.commit()
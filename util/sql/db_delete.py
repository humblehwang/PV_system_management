from util.sql.db_init import db, Record_data, Tel_Record, Ctbl_Record

def del_recordDataByProNum(project_number) -> str:
	# get the project number
	try:
		Record_data.query.filter_by(pro_num=project_number).delete()
		db.session.commit()
		return None
	except Exception as err:
		return err

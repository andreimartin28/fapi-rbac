from fastapi import APIRouter, status, HTTPException, Depends
from configs.db import db
from controllers.auth.oauth2 import get_current_user
import bcrypt
from libraries.validations import alphanumeric, password

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/')
def create_user(user_username: str, user_password: str):
    if not alphanumeric(user_username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="The username format is not valid")
    if not password(user_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "The password format is not valid. Minimum eight characters,\
                at least one letter, one number and one special character"
            )
        )

    hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')
    check_username_existence = db.select('''select count(*) from rbac_fastapi.users where user_username = '{0}';'''.format("".join(user_username)))
    if check_username_existence['count(*)'] > 0:
        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail='The username is already taken'
                            )
    else:
        db.insert(''' insert into rbac_fastapi.users (user_username, user_password) values('{0}','{1}');'''.format(user_username, hashed_password))
        return {
                "user_username": user_username,
                "user_password": hashed_password
                }


@router.get('/all',
            summary='Retrieve all the existent users from the database',
            description='Click on execute to get the data',
            response_description='All the users existent')
def get_all_users(current_user_data: str = Depends(get_current_user)):
    if not current_user_data['role_name'] == 'superadmin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have the permission to perform this operation")
    all_users_data = db.select(
        ''' select user_id, user_username, user_password
            from rbac_fastapi.users; ''',
        selectOnce=False)

    if not all_users_data:
        raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No users found")
    print({"all_user_data": all_users_data})
    users_list = [
        {
            "user_id": user['user_id'],
            "user_username": user['user_username'],
        }
        for user in all_users_data
    ]
    return {"users": users_list}


@router.get('/{user_id}')
def get_user(user_id: int, current_user_data: str = Depends(get_current_user)):
    if not (current_user_data['role_name'] == 'superadmin' or current_user_data[user_id] == user_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have the permission to perform this operation"
        )
    check_user_existence = db.select(''' select count(*) from rbac_fastapi.users where user_id = '{0}'; '''.format(user_id))
    if check_user_existence['count(*)'] == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="The user with " +
                            f"user_id = {user_id} not found")
    user_data = db.select(''' select user_id, user_username, user_password from rbac_fastapi.users where user_id = {0}; '''.format(user_id))
    if user_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    return {"user_username": user_data['user_username'],
            "user_password": user_data['user_password']
            }


@router.put('/{user_id}')
def update_user(user_id: int,
                user_username: str,
                user_password: str,
                current_user_data: str = Depends(get_current_user)):
    if not (current_user_data['role_name'] == 'admin' or current_user_data['role_name'] == 'superadmin' or current_user_data['user_id'] == user_id):
        raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="You do not have the permission to perform this operation"
                        )

    if not alphanumeric(user_username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="The username format is not valid")

    if not password(user_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="The password format is not valid. " +
                            "Minimum eight characters, at least one letter, " +
                            "one number and one special character")
    hshd_pwd = bcrypt.hashpw(
                            user_password.encode('utf-8'),
                            bcrypt.gensalt(rounds=12)
                            )
    check_username_existence = db.select(''' select count(*) from rbac_fastapi.users where user_username = '{0}' and user_id != '{1}';'''.format(user_username, user_id)) 
    if check_username_existence['count(*)'] > 0:
        raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail='The username is already taken'
                        )
    db.update(''' update rbac_fastapi.users set user_username='{0}', user_password='{1}' where user_id = '{2}'; '''.format(user_username, hshd_pwd.decode('utf-8'), user_id))
    return {
            "user_id": user_id,
            "user_username": user_username,
            "user_password": hshd_pwd.decode('utf-8')
            }


@router.delete('/{user_id}')
def delete_user(
                user_id: int,
                current_user_data: str = Depends(get_current_user)
                ):
    if not (current_user_data['role_name'] == 'superadmin' or current_user_data['role_name'] == 'admin' or current_user_data['user_id'] == user_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You are not allowed " +
                            "to delete this data!")
    check_user_existence = db.select(''' select count(*) from rbac_fastapi.users where user_id = '{0}' '''.format(user_id))
    print({'check_user_existence': check_user_existence})
    if check_user_existence['count(*)'] == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="The user with " +
                            f"user_id = {user_id} was not found or it has " +
                            "already been deleted.")

    db.delete(''' delete from rbac_fastapi.users where user_id='{0}'; '''.format(user_id))

    return {
            "data_info": f"The user with user_id = {user_id} has " +
            "been deleted successfully!"
            }

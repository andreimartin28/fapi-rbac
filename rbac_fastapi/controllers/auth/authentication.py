from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from controllers.auth.oauth2 import get_user_data_by_username, create_jwt_token
import bcrypt

router = APIRouter(prefix='', tags=['authentication'])


@router.post('/token')
def get_token(request: OAuth2PasswordRequestForm = Depends()):
    user_data = get_user_data_by_username(request.username)
    if user_data is not None:
        verify_password = bcrypt.checkpw(
            request.password.encode('utf-8'),
            user_data['user_password'].encode('utf-8')
            )
        if not (user_data['user_username'] == request.username
                and verify_password == 1):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid credentials. Username " +
                                "or password invalid")
        else:
            access_token = create_jwt_token(data={"sub": request.username})
            return {
                    "access_token": access_token,
                    "token-type": "bearer",
                    "user_id": user_data['user_id'],
                    "user_username": request.username
                    }
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found or not existent")

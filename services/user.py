from sqlalchemy.orm import Session

from models.user import User as UserModel


def get_user_by_id(db: Session, user_id: int):
    """Get the user with specific id."""
    return db.query(UserModel).get(user_id)


def get_user_by_email(db: Session, email: str):
    """Get the user with specific id."""
    return db.query(UserModel).filter(UserModel.email == email).first()


def create_user(db: Session, user: UserModel) -> UserModel:
    db_user: UserModel = UserModel(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> UserModel:
    user = get_user_by_id(db, user_id)
    if user:
        db.delete(user)
        db.commit()
    return user

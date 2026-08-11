from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    @staticmethod
    def get_by_email(db: Session, email: str):
        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    @staticmethod
    def create(db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_by_id(db: Session, user_id):
        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )
    @staticmethod
    def update_password(
        db: Session,
        user: User,
        hashed_password: str
    ):
        user.password = hashed_password
        db.commit()
        db.refresh(user)
        return user
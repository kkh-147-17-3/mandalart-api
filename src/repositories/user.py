from enums import SocialProvider
from repositories.base import BaseRepository
from schemas.user import User


class UserRepository(BaseRepository[User]):
    def get_user_by_social_id_and_provider(self, social_id: str, provider: SocialProvider) -> User:
        user = (self.db.query(User).filter(User.social_id == social_id)
                .filter(User.social_provider == provider)
                .first())

        if user is None:
            user = User(social_id=social_id, social_provider=provider)
            self.db.add(user)
            self.db.commit()
        return user

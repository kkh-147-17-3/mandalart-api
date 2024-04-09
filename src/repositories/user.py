from enums import SocialProvider
from repositories.base import BaseRepository
from schemas.user import User


class UserRepository(BaseRepository[User]):
    def find_by_social_provider_and_social_id(self, social_id: str,
                                              social_provider: SocialProvider) -> User | None:
        return self._db.query(User).filter(User.social_id == social_id).filter(
            User.social_provider == social_provider).order_by(User.id.desc()).first()

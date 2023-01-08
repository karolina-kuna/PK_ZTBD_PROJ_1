from bson import ObjectId

from market_app.models.api_models import OwnerApiModel
from market_app.models.db_models.fast_api_mongodb_models import OwnerModel


class MongoDbMapper:

    @staticmethod
    def map_owner_api_model_to_owner_model(api_model: OwnerApiModel) -> OwnerModel:
        return OwnerModel(
            id=ObjectId() if not api_model.owner_id else api_model.owner_id,
            name=api_model.name,
            surname=api_model.surname,
            phone_number=api_model.phone_number,
            address=api_model.address,
            email_address=api_model.email_address,
            company_name=api_model.company_name
        )

    @staticmethod
    def map_owner_model_to_owner_api_model(model: OwnerModel) -> OwnerApiModel:
        return OwnerApiModel(
            owner_id=str(model.id),
            name=model.name,
            surname=model.surname,
            phone_number=model.phone_number,
            address=model.address,
            email_address=model.email_address,
            company_name=model.company_name
        )
